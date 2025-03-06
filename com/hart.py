
class HARTconnector:
    def __init__(self, address):
        self.address = address

    def changeAddress(self, address):
        self.address = address

    def getRequestMessage(self, command, data=None):
        if data is None:
            data = []
        message = []
        # Preamble (5-20 bytes)
        for _ in range(5):
            message.append(0xFF)
        # startByte (1 byte)
        message.append(0x82)
        # address (1 or 5 byte)
        message.append(0x80 | self.address)
        #Expansion (4 bytes)
        for _ in range(4):
            message.append(0)
        # command (1 byte)
        message.append(command)
        # count (1 byte)
        message.append(len(data))
        # checkSum (1 byte)
        message.append(self.getCheckSum(message[5:]))
        return bytes(message)

    @staticmethod
    def getByteList(data, length):
        result = []
        length -= 1
        mask = 0xFF << (length * 8)
        for i in range(length, -1, -1):
            result.append((data & mask) >> (i * 8))
            mask >>= 8
        return result

    @staticmethod
    def getCheckSum(data: list):
        result = 0x00
        for b in data:
            result ^= b
        return result

    def readUniqueIdentifier(self):
        message = self.getRequestMessage(0)
        return message, len(message) + 18

    def readPrimaryVariable(self):
        message = self.getRequestMessage(1)
        return message, len(message) + 7

    def readCurrentAndPercentOfRange(self):
        message = self.getRequestMessage(2)
        return message, len(message) + 10

    def readTagDescriptorDate(self):
        message = self.getRequestMessage(13)
        return message, len(message) + 23

    def readOutputInformation(self):
        message = self.getRequestMessage(15)
        return message, len(message) + 19

