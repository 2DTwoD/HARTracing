import threading


class ComDict(dict):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.__setitem__("measure", None)
        self.__setitem__("current", None)
        self.__setitem__("percent", None)
        self.__setitem__("sensorStatus",  None)
        self.__setitem__("hartStatus", None)
        self.__setitem__("unit", None)
        self.__setitem__("tag", "--------")
        self.__setitem__("descriptorDate", None)
        self.__setitem__("rangeUnit", None)
        self.__setitem__("4mA", None)
        self.__setitem__("20mA", None)

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
