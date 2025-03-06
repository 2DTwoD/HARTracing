import threading
import time

from serial.serialutil import SerialException

from com.hart import HARTconnector

import serial.tools.list_ports
import serial

from misc.types import CommStatus


class Com:
    def __init__(self):
        super().__init__()
        self.thread = None
        self.port = None
        self.cycleIndex = 0
        self.errorCounter = 0
        self.sendCommand = []
        self.start = False
        self.status = CommStatus.DISCONNECT
        self.hartConnector = HARTconnector(0)
        self.cycleCommands = [self.hartConnector.readUniqueIdentifier,
                              self.hartConnector.readPrimaryVariable,
                              self.hartConnector.readCurrentAndPercentOfRange,
                              self.hartConnector.readTagDescriptorDate,
                              self.hartConnector.readOutputInformation]

        #Скорость передачи (1200)
        self.baudrate = 1200
        #Четность (Odd)
        self.parity = "O"
        #Стоповые биты (=1)
        self.stopBits = 1
        #Период обмена, сек
        self.sendPeriod = 0.1
        #Время возникновения ошибки передачи, если нет ответа, сек
        self.readTimeOut = 0.5
        #Разное
        self.bufferSize = 10
        self.maxCountForErrorVis = 20

        self.errorCounter = self.maxCountForErrorVis

    def send(self, command: str):
        if self.disconnected():
            return
        if command not in self.sendCommand:
            self.sendCommand.append(command)

    def runSending(self, device: str):
        try:
            self.port = serial.Serial(device, baudrate=self.baudrate, parity=self.parity, stopbits=self.stopBits)
            self.port.timeout = self.readTimeOut

            while self.start:
                # time.sleep(self.sendPeriod)

                self.port.reset_input_buffer()
                self.port.reset_output_buffer()

                if self.sendCommand:
                    self.port.write(self.sendCommand.pop(0)())
                    resp = self.port.read(self.bufferSize)
                    continue
                else:
                    command = self.cycleCommands[self.cycleIndex]()
                    self.port.write(command[0])
                    resp = self.port.read(command[1])
                    print(command)
                    print(resp)

                self.cycleIndex += 1
                if self.cycleIndex >= len(self.cycleCommands):
                    self.cycleIndex = 0

                if self.status != CommStatus.CONNECT:
                    self.errorCounter -= 1
                    if self.errorCounter <= 0:
                        self.status = CommStatus.CONNECT
                        self.errorCounter = self.maxCountForErrorVis

        except SerialException:
            self.status = CommStatus.LINK_ERROR
        else:
            self.status = CommStatus.DISCONNECT
        finally:
            if self.port is not None:
                self.port.close()

    def checkResponse(self, read, startChar, endChar, content=None):
        try:
            start = read.index(startChar)
            end = read.index(endChar)

            if start == -1 or end == -1:
                return True, None

            subString = read[start: end +1]

            if content is not None and subString != content:
                return True, None

            return False, subString
        except:
            return True, None

    @staticmethod
    def getAvailablePorts():
        result = []
        ports = serial.tools.list_ports.comports()
        for port in ports:
            result.append(port.device)
        return result

    def connect(self, device: str):
        self.status = CommStatus.CONNECT
        if self.connected():
            return
        self.thread = threading.Thread(target=self.runSending, args=(device, ))
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