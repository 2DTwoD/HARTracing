import struct

from misc.types import MessageType

codeToASCIIstr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
codeToASCIIstr2 = "@ABCDEFGHIJKLMNOPQRSTUVWXYZ[ ]^_ ! #$%&'()*+'-./0123456789:;<=>?"

ASCIItoCodeDict = {
    'A': 0, 'Q': 16, 'g': 32, 'w': 48,
    'B': 1, 'R': 17, 'h': 33, 'x': 49,
    'C': 2, 'S': 18, 'i': 34, 'y': 50,
    'D': 3, 'T': 19, 'j': 35, 'z': 51,
    'E': 4, 'U': 20, 'k': 36, '0': 52,
    'F': 5, 'V': 21, 'l': 37, '1': 53,
    'G': 6, 'W': 22, 'm': 38, '2': 54,
    'H': 7, 'X': 23, 'n': 39, '3': 55,
    'I': 8, 'Y': 24, 'o': 40, '4': 56,
    'J': 9, 'Z': 25, 'p': 41, '5': 57,
    'K': 10, 'a': 26, 'q': 42, '6': 58,
    'L': 11, 'b': 27, 'r': 43, '7': 59,
    'M': 12, 'c': 28, 's': 44, '8': 60,
    'N': 13, 'd': 29, 't': 45, '9': 61,
    'O': 14, 'e': 30, 'u': 46, '+': 62,
    'P': 15, 'f': 31, 'v': 47, '/': 63
}


class HARTconnector:
    def __init__(self, address):
        self.address = address

    def changeAddress(self, address):
        self.address = address

    def getRequestMessage(self, command, data=None):
        if data is None:
            data = []
        message = []
        # Preamble (5 bytes)
        for _ in range(5):
            message.append(0xFF)
        # startByte (1 byte)
        message.append(0x82)
        # address (1)
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
    def getCheckSum(data):
        result = 0x00
        for b in data:
            result ^= b
        return result

    def getCommandAndLength(self, messageType: MessageType):
        message = self.getRequestMessage(messageType.value["commandNumber"])
        return message, len(message) + messageType.value["dataLen"] + 2

    @staticmethod
    def parseResponse(response: bytes, messageType: MessageType):
        try:
            receivedCheckSum = response[-1]
            calculatedCheckSum = HARTconnector.getCheckSum(response[5:-1])
            if messageType == MessageType.READ_UNIQUE_IDENTIFIER:
                pass
            if receivedCheckSum != calculatedCheckSum:
                raise Exception("Wrong check sum")
            status = response[13:15]
            result = {"sensorStatus": (status[1] >> 7) > 0, "hartStatus": (status[0] & 0x7F) > 0}
            data = response[15: 15 + messageType.value["dataLen"]]
            if messageType == MessageType.READ_UNIQUE_IDENTIFIER:
                result["manuf"] = data[1]
                result["devType"] = data[2]
                result["soft"] = data[6]
                result["hard"] = data[7]
            elif messageType == MessageType.READ_PRIMARY_VARIABLE:
                result["unit"] = data[0]
                result["measure"] = round(struct.unpack('f', data[4: 0: -1])[0], 3)
            elif messageType == MessageType.READ_CURRENT_AND_PERCENT_OF_RANGE:
                result["current"] = round(struct.unpack('f', data[3:: -1])[0], 2)
            elif messageType == MessageType.READ_TAG_DESCRIPTOR_DATE:
                result["tag"] = HARTconnector.getASCIIstr(data[0:6])
            elif messageType == MessageType.READ_OUTPUT_INFORMATION:
                result["4mA"] = round(struct.unpack('f', data[10: 6: -1])[0], 3)
                result["20mA"] = round(struct.unpack('f', data[6: 2: -1])[0], 3)
            return result
        except:
            return {}

    @staticmethod
    def getASCIIstr(data: bytes):
        result = ""
        big = 0
        for i, b in enumerate(data):
            big |= (b << 8 * i)
        for _ in range(8):
            result += codeToASCIIstr2[big & 0x3F]
            big >>= 6
        return result
