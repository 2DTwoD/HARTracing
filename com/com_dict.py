class ComDict(dict):
    def __init__(self):
        super().__init__()
        self.__setitem__("manuf", 0x00)
        self.__setitem__("model", 0x00)
        self.__setitem__("soft", 0x00)
        self.__setitem__("hard", 0x00)
        self.__setitem__("measure", 0x00)
        self.__setitem__("current", 0x00)
        self.__setitem__("sensorStatus", 0x00)
        self.__setitem__("hartStatus", 0x00)
        self.__setitem__("unit", 0x00)
        self.__setitem__("tag", 0x00)
        self.__setitem__("4mA", 0x00)
        self.__setitem__("20mA", 0x00)
