import threading


class ComDict(dict):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.__setitem__("manuf", 0x01)
        self.__setitem__("model", 0x01)
        self.__setitem__("soft", 0x01)
        self.__setitem__("hard", 0x01)
        self.__setitem__("measure", 0x01)
        self.__setitem__("current", 0x01)
        self.__setitem__("sensorStatus", True)
        self.__setitem__("hartStatus", True)
        self.__setitem__("unit", "Попугаи")
        self.__setitem__("tag", "XXXXXXXX")
        self.__setitem__("4mA", 0x01)
        self.__setitem__("20mA", 0x01)

    def set(self, key, value):
        with self.lock:
            if str(key) in self.keys():
                self[key] = value

    def getValue(self, key):
        with self.lock:
            return self[key]
