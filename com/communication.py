import threading
import time
from enum import Enum

from serial.serialutil import SerialException

from com.hart import HARTconnector, MessageType, DeleteFlag, FrameType

import serial.tools.list_ports
import serial

from misc import di


class CommStatus(Enum):
    CONNECT = "V"
    DISCONNECT = "X"
    LINK_ERROR = "Ош. связи"
    RECEIVE_ERROR = "Ош. передачи"


class Com:
    def __init__(self):
        super().__init__()
        self.comDict = di.Container.comDict()
        self.thread = None
        self.port = None
        self.lock = threading.Lock()
        self.cycleIndex = 0
        self.start = False
        self.status = CommStatus.DISCONNECT
        self.cycleCommandSeq = []
        self.hartConnector = HARTconnector()
        self.firstScan = False
        self.dataReaded = True

        # Имя порта (=COM?)
        self.device = "COM1"
        # Скорость передачи (=1200)
        self.baudrate = 1200
        # Четность (=Odd)
        self.parity = "O"
        # Стоповые биты (=2)
        self.stopBits = 2
        # Время приема сообщения, сек
        self.recvPeriod = 0.3

    def send(self, messageType: MessageType, data=None):
        if self.disconnected():
            return
        with self.lock:
            self.cycleCommandSeq.append((messageType, data))
            if messageType == MessageType.WRITE_TAG_DESCRIPTOR_DATE:
                self.cycleCommandSeq.append((MessageType.READ_TAG_DESCRIPTOR_DATE, None))
            else:
                self.cycleCommandSeq.append((MessageType.READ_OUTPUT_INFORMATION, None))

    def runSending(self):
        try:
            self.port = serial.Serial(self.device, baudrate=self.baudrate, parity=self.parity, stopbits=self.stopBits)
            self.port.timeout = 0

            while self.start:
                self.port.reset_input_buffer()
                self.port.reset_output_buffer()
                with self.lock:
                    messageType, data = self.cycleCommandSeq[self.cycleIndex]
                command = self.hartConnector.getCommand(messageType, data=data)

                self.port.write(command)
                response = bytearray()
                while 1:
                    time.sleep(self.recvPeriod)
                    b = self.port.readall()
                    if b == b'':
                        break
                    response.extend(b)

                result = self.hartConnector.parseResponse(response, messageType)
                if result is None:
                    self.status = CommStatus.RECEIVE_ERROR
                    if messageType.value["deleteFlag"] == DeleteFlag.ONCE:
                        self.deleteItem()
                else:
                    self.status = CommStatus.CONNECT
                    self.comDict.setAll(result)
                    if messageType.value["deleteFlag"] != DeleteFlag.NEVER:
                        self.deleteItem()
                    else:
                        self.cycleIndex += 1

                if self.cycleIndex >= len(self.cycleCommandSeq):
                    self.cycleIndex = 0
                    self.firstScan = False

        except SerialException:
            self.status = CommStatus.LINK_ERROR
        else:
            self.status = CommStatus.DISCONNECT
        finally:
            if self.port is not None:
                self.port.close()

    def deleteItem(self):
        with self.lock:
            del self.cycleCommandSeq[self.cycleIndex]

    @staticmethod
    def getAvailablePorts():
        result = []
        ports = serial.tools.list_ports.comports()
        for port in ports:
            result.append(port.device)
        return result

    def connect(self, device: str, baudrate=1200, parity="O", stopBits=1):
        self.status = CommStatus.CONNECT
        if self.connected():
            return

        self.device = device
        self.baudrate = baudrate
        self.parity = parity
        self.stopBits = stopBits

        self.cycleCommandSeq = [(MessageType.READ_UNIQUE_IDENTIFIER, None),
                                (MessageType.READ_CURRENT_AND_PERCENT_OF_RANGE, None),
                                (MessageType.READ_TAG_DESCRIPTOR_DATE, None),
                                (MessageType.READ_PRIMARY_VARIABLE, None),
                                (MessageType.READ_OUTPUT_INFORMATION, None)]
        self.hartConnector.fillAddressZero()
        self.firstScan = True
        self.dataReaded = False
        self.thread = threading.Thread(target=self.runSending)
        self.thread.daemon = True
        self.start = True
        self.thread.start()

    def disconnect(self):
        self.start = False
        self.status = CommStatus.DISCONNECT

    def connected(self):
        return self.port is not None and self.port.is_open and self.thread.is_alive()

    def disconnected(self):
        return not self.connected()

    def getStatus(self):
        return self.status.value

    def firstTimeDataReady(self):
        result = not self.firstScan and not self.dataReaded
        if not self.firstScan and self.connected():
            self.dataReaded = True
        return result

