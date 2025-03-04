# import hart_protocol.universal
# import serial
# from hart_protocol import *
#
#
# def getMessage(address, command):
#     message = []
#     # Preamble (5-20 bytes)
#     for _ in range(5):
#         message.append(0xFF)
#     # startByte (1 byte)
#     message.append(0x02)
#     # address (1 or 5 byte)
#     message.append(0x80 | address)
#     #Expansion
#     for _ in range(4):
#         message.append(0)
#     # command (1 byte)
#     message.append(command)
#     # count (1 byte)
#     message.append(0)
#     # checkSum (1 byte)
#     message.append(getCheckSum(message[5:]))
#     return bytes(message)
#
#
# def getByteList(data, length):
#     result = []
#     for i in range(length):
#         result.append(data & 0xFF)
#         data >>= (8 * (i + 1))
#     result.reverse()
#     return result
#
#
# def getCheckSum(data: list):
#     result = 0x00
#     for b in data:
#         result ^= b
#     # for b in data:
#     #     result = ((result + b) & 0xFF)
#     # return ((result ^ 0xFF) + 1) & 0xFF
#     return result
#
#
# with serial.Serial('COM6', 1200, timeout=1, parity="O", stopbits=1) as ser:
#     # mes = hart_protocol.universal.read_primary_variable(0)
#     # ser.write(mes)
#     # resp = ser.read(100)
#     # print(mes)
#     # print(resp)
#     msg = getMessage(0, 1)
#     ser.write(msg)
#     data = ser.read(100)
#     print(msg)
#     print(data)
import sys

from PyQt6.QtWidgets import QApplication

from misc import di

version = "v1.0.0"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = di.Container.mainWindow(version=version, windowWidth=800, windowHeight=300, windowLabel="HARTracing")
    window.init()
    app.exec()
