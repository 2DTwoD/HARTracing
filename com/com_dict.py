import threading

from misc.types import MessageType


class ComDict(dict):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.__setitem__("manuf", 0x00)
        self.__setitem__("devType", 0x00)
        self.__setitem__("soft", 0x00)
        self.__setitem__("hard", 0x00)
        self.__setitem__("measure", 0x00)
        self.__setitem__("current", 0x00)
        self.__setitem__("sensorStatus",  True)
        self.__setitem__("hartStatus", True)
        self.__setitem__("unit", "XXX")
        self.__setitem__("tag", "XXXXXXXX")
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


