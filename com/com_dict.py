import threading


class ComDict(dict):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.__setitem__("measure", 0x00)
        self.__setitem__("current", 0x00)
        self.__setitem__("percent", 0x00)
        self.__setitem__("sensorStatus",  0x00)
        self.__setitem__("hartStatus", 0x00)
        self.__setitem__("unit", 252)
        self.__setitem__("tag", "--------")
        self.__setitem__("descriptorDate", None)
        self.__setitem__("4mA", 0x00)
        self.__setitem__("20mA", 0x00)

    def set(self, key, value):
        with self.lock:
            if str(key) in self.keys():
                self[key] = value
                return True
            return False

    def setAll(self, newDict: dict):
        for key in newDict.keys():
            if str(key) not in self.keys():
                return False
        with self.lock:
            self.update(newDict)
            return True

    def getValue(self, key):
        with self.lock:
            if str(key) in self.keys():
                return self[key]
            return None
