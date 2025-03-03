from dependency_injector import containers, providers

from panels.main_window import MainWindow


class Container(containers.DeclarativeContainer):
    mainWindow = providers.Singleton(MainWindow)
