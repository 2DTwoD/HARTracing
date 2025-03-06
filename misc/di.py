from dependency_injector import containers, providers

from com.com_dict import ComDict
from com.communication import Com


class Container(containers.DeclarativeContainer):
    com = providers.Singleton(Com)
    comDict = providers.Singleton(ComDict)
