import struct
from enum import Enum

codeToASCIIstr = r"""@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_ !"#$%&'()*+,-./0123456789:;<=>?"""

ASCIItoCodeDict = {
    'A': 1, 'Q': 17, '!': 33, '1': 49,
    'B': 2, 'R': 18, '"': 34, '2': 50,
    'C': 3, 'S': 19, '#': 35, '3': 51,
    'D': 4, 'T': 20, '$': 36, '4': 52,
    'E': 5, 'U': 21, '%': 37, '5': 53,
    'F': 6, 'V': 22, '&': 38, '6': 54,
    'G': 7, 'W': 23, '\'': 39, '7': 55,
    'H': 8, 'X': 24, '(': 40, '8': 56,
    'I': 9, 'Y': 25, ')': 41, '9': 57,
    'J': 10, 'Z': 26, '*': 42, ':': 58,
    'K': 11, '[': 27, '+': 43, ';': 59,
    'L': 12, '\\': 28, ',': 44, '<': 60,
    'M': 13, ']': 29, '-': 45, '=': 61,
    'N': 14, '^': 30, '.': 46, '>': 62,
    'O': 15, '_': 31, '/': 47, '?': 63,
    'P': 16, ' ': 32, '0': 48, '@': 0
}

unitDict = {
    # Temperature:
    "°C": 32, "°F": 33, "°R": 34, "K": 35,
    # Pressure:
    "inH2O": 1, "inHg": 2, "ftH2O": 3, "mmH2O": 4, "mmHg": 5,
    "psi": 6, "bar": 7, "mbar": 8, "g/cm2": 9, "kg/cm2": 10,
    "Pa": 11, "kPa": 12, "Torr": 13, "atm": 14, "inH20(60 °F)": 145,
    "MPa": 237, "inH2O (4 °C)": 238, "mmH2O (4 °C)": 239,
    # Volumetric flow:
    "ft3/min": 15, "gal/min": 16, "l/min": 17, "gal (UK)/min": 18,
    "m3/h": 19, "gal/s": 22, "Mgal/d": 23, "l/s": 24, "Ml/d": 25,
    "ft3/s": 26, "ft3/d": 27, "m3/s": 28, "m3/d": 29, "gal (UK)/h": 30,
    "gal (UK)/d": 31, "Nm3/h": 121, "Nl/h": 122, "SCF/min": 123,
    "ft3/h": 130, "m3/min": 131, "bbl/sec": 132, "bbl/min": 133,
    "bbl/h": 134, "bbl/d": 135, "gal/h": 136, "gal (UK)/s": 137,
    "l/h": 138, "gal/d": 235,
    # Velocity:
    "ft/s": 20, "m/s": 21, "in/s": 114, "in/min": 115, "ft/min": 116,
    "m/h": 120,
    # Volume:
    "gal": 40, "l": 41, "gal (UK)": 42, "m3": 43, "bbl": 46, "bu": 110,
    "yd3": 111, "ft3": 112, "in3": 113, "bbl (US)": 124, "Nm3": 166,
    "Nl": 167, "SCF": 168, "hl": 236,
    # Length:
    "ft": 44, "m": 45, "in": 47, "cm": 48, "mm": 49, "ft-16": 151,
    # Time:
    "min": 50, "s": 51, "h": 52, "d": 53,
    # Mass:
    "g": 60, "kg": 61, "t": 62, "lb": 63, "ton": 64, "ton (UK)": 65,
    "oz": 125,
    # Mass Flow:
    "g/s": 70, "g/min": 71, "g/h": 72, "kg/s": 73, "kg/m": 74, "kg/h": 75,
    "kg/d": 76, "t/min": 77, "t/h": 78, "t/d": 79, "lb/s": 80, "lb/min": 81,
    "lb/h": 82, "lb/d": 83, "ton/min": 84, "tom/h": 85, "ton/d": 86,
    "ton (UK)/h": 87, "ton (UK)/d": 88,
    # Mass per Volume:
    "SG": 90, "g/cm3": 91, "kg/m3": 92, "lb/gal": 93, "lb/ft3": 94,
    "g/ml": 95, "kg/l": 96, "g/l": 97, "lb/in3": 98, "ton/yd3": 99,
    "°Tw": 100, "B°": 102, "B° (light)": 103, "Degrees API": 104,
    "μg/l": 146, "μg/m3": 147,
    # Viscosity:
    "cSt": 54, "cP": 55,
    # Electromagnetic Unit Of Electrical Potential:
    "mV": 36, "V": 58,
    # Electrostatic Unit Of Current:
    "mA": 39,
    # Electromagnetic Unit Of Resistance:
    "Ω": 37, "kΩ": 163,
    # Energy:
    "J": 69, "DTH": 89, "ft*lbf": 126, "kWh": 128, "Mcal (th)": 162,
    "MJ": 164, "Btu": 165,
    # Power:
    "kW": 127, "hp": 129, "Mcal (th)/h": 140, "MJ/h": 141, "Btu/h": 142,
    # Radial Velocity:
    "°/s": 117, "rps": 118, "rpm": 119,
    # Miscellanious:
    "Hz": 38, "%": 57, "pH": 59, "°Bx": 101, "%w": 105, "%v": 106,
    "°Bg": 107, "proof/vol": 108, "proof/mass": 109, "ppm": 139,
    "%c": 148, "%q": 150, "ft3/lb": 152, "pF": 153, "ml/l": 154,
    "dB": 156, "°P": 160, "%LEL": 161, "ppb": 169,
    # Unknown
    "unknown": 252
}

preambleLen = 5

class FrameType(Enum):
    SHORT = 0x02
    LONG = 0x82


class DeleteFlag(Enum):
    NEVER = 0
    SUCCESS = 1
    ONCE = 2


class MessageType(Enum):
    READ_UNIQUE_IDENTIFIER = {"commandNumber": 0, "dataLen": 12, "deleteFlag": DeleteFlag.SUCCESS, "frameType": FrameType.SHORT}
    READ_PRIMARY_VARIABLE = {"commandNumber": 1, "dataLen": 5, "deleteFlag": DeleteFlag.NEVER, "frameType": FrameType.LONG}
    READ_CURRENT_AND_PERCENT_OF_RANGE = {"commandNumber": 2, "dataLen": 8, "deleteFlag": DeleteFlag.NEVER, "frameType": FrameType.LONG}
    READ_TAG_DESCRIPTOR_DATE = {"commandNumber": 13, "dataLen": 21, "deleteFlag": DeleteFlag.SUCCESS, "frameType": FrameType.LONG}
    READ_OUTPUT_INFORMATION = {"commandNumber": 15, "dataLen": 17, "deleteFlag": DeleteFlag.SUCCESS, "frameType": FrameType.LONG}
    WRITE_TAG_DESCRIPTOR_DATE = {"commandNumber": 18, "dataLen": 21, "deleteFlag": DeleteFlag.ONCE, "frameType": FrameType.LONG}
    WRITE_RANGE_VALUES = {"commandNumber": 35, "dataLen": 9, "deleteFlag": DeleteFlag.ONCE, "frameType": FrameType.LONG}
    SET_UPPER_RANGE_VALUE = {"commandNumber": 36, "dataLen": 0, "deleteFlag": DeleteFlag.ONCE, "frameType": FrameType.LONG}
    SET_LOWER_RANGE_VALUE = {"commandNumber": 37, "dataLen": 0, "deleteFlag": DeleteFlag.ONCE, "frameType": FrameType.LONG}
    SET_TRIM_PV_ZERO = {"commandNumber": 43, "dataLen": 0, "deleteFlag": DeleteFlag.ONCE, "frameType": FrameType.LONG}
    WRITE_PV_UNITS = {"commandNumber": 44, "dataLen": 1, "deleteFlag": DeleteFlag.ONCE, "frameType": FrameType.LONG}


class HARTconnector:
    def __init__(self):
        self.addressList = [0, 0, 0, 0, 0]

    def getRequestMessage(self, command, frameType=FrameType.SHORT, data=None):
        if data is None:
            data = []
        message = []
        # Preamble (5 bytes)
        for _ in range(preambleLen):
            message.append(0xFF)
        # startByte (1 byte)
        message.append(frameType.value)
        # address (1 byte)
        message.append(0x80 | self.addressList[0])
        if frameType == FrameType.LONG:
            # expansion (4 bytes)
            for i in range(1, 5):
                message.append(self.addressList[i])
        # command (1 byte)
        message.append(command)
        # count (1 byte)
        message.append(len(data))
        # data (X bytes)
        if data is not None:
            message.extend(data)
        # checkSum (1 byte)
        message.append(self.getCheckSum(message[5:]))
        return bytes(message)

    def updateAddressList(self, idCode=0, typeCode=0, idNumB1=0, idNumB2=0, idNumB3=0):
        self.addressList[0] = idCode & 0x3F
        self.addressList[1] = typeCode
        self.addressList[2] = idNumB1
        self.addressList[3] = idNumB2
        self.addressList[4] = idNumB3

    def getCommand(self, messageType: MessageType, data=None):
        return self.getRequestMessage(messageType.value["commandNumber"],
                                      frameType=messageType.value["frameType"],
                                      data=data)

    def parseResponse(self, response: bytes, messageType: MessageType):
        try:
            respPreamble = 0
            for b in response:
                if b != 0xFF:
                    break
                respPreamble += 1
            expansionLen = 4 if messageType.value["frameType"] == FrameType.LONG else 0
            count = response[respPreamble + 3 + expansionLen]
            dataLen = count - 2
            messageLength = respPreamble + 7 + expansionLen + dataLen
            receivedCheckSum = response[messageLength - 1]
            calculatedCheckSum = HARTconnector.getCheckSum(response[respPreamble:messageLength - 1])

            if receivedCheckSum != calculatedCheckSum:
                raise Exception("Wrong check sum")

            status = response[9 + expansionLen: 11 + expansionLen]
            result = {"sensorStatus": (status[1] >> 7) > 0, "hartStatus": (status[0] & 0x7F) > 0}
            data = response[11 + expansionLen: 11 + expansionLen + dataLen]

            if messageType == MessageType.READ_UNIQUE_IDENTIFIER:
                self.updateAddressList(idCode=data[1], typeCode=data[2],
                                       idNumB1=data[9], idNumB2=data[10], idNumB3=data[11])
            elif messageType == MessageType.READ_PRIMARY_VARIABLE:
                result["unit"] = data[0]
                result["measure"] = round(struct.unpack('>f', data[1:])[0], 3)
            elif messageType == MessageType.READ_CURRENT_AND_PERCENT_OF_RANGE:
                result["current"] = round(struct.unpack('>f', data[0: 4])[0], 2)
                result["percent"] = round(struct.unpack('>f', data[4:])[0], 1)
            elif messageType == MessageType.READ_TAG_DESCRIPTOR_DATE:
                result["tag"] = HARTconnector.getASCIIstr(data[0:6])
                result["descriptorDate"] = data[6:]
            elif messageType == MessageType.READ_OUTPUT_INFORMATION:
                result["4mA"] = round(struct.unpack('>f', data[7: 11])[0], 3)
                result["20mA"] = round(struct.unpack('>f', data[3: 7])[0], 3)
            return result
        except:
            return None

    @staticmethod
    def getCheckSum(data):
        result = 0x00
        for b in data:
            result ^= b
        return result

    @staticmethod
    def getLongitudinalRedundancyCheck(data):
        result = 0x00
        for b in data:
            result = (result + b) & 0xFF
        result = (((result ^ 0xFF) + 1) & 0xFF)
        return result

    @staticmethod
    def getASCIIstr(data: bytes):
        return (HARTconnector.getFourSymbolsFromThreeBytes(data[0:3]) +
                HARTconnector.getFourSymbolsFromThreeBytes(data[3:]))

    @staticmethod
    def getFourSymbolsFromThreeBytes(data: bytes) -> str:
        result = ""
        if len(data) != 3:
            return "----"
        result += codeToASCIIstr[(data[0] >> 2)]
        result += codeToASCIIstr[((data[0] & 0x3) << 4) | (data[1] >> 4)]
        result += codeToASCIIstr[((data[1] & 0xF) << 2) | (data[2] >> 6)]
        result += codeToASCIIstr[data[2] & 0x3F]
        return result

    @staticmethod
    def getTreeBytesFromFourSymbols(text: str) -> bytearray:
        result = bytearray()
        textList = list(text)
        for i, c in enumerate(textList):
            if c not in ASCIItoCodeDict.keys():
                textList[i] = '-'
        if len(textList) != 4:
            return result
        result.append((ASCIItoCodeDict[textList[0]] << 2) | (ASCIItoCodeDict[textList[1]] >> 4))
        result.append(((ASCIItoCodeDict[textList[1]] & 0xF) << 4) | (ASCIItoCodeDict[textList[2]] >> 2))
        result.append(((ASCIItoCodeDict[textList[2]] & 0x3) << 6) | ASCIItoCodeDict[textList[3]])
        return result
