import sys

from logging import getLogger
from PySide6.QtWidgets import QApplication

from .windows import MainWindow


class AppComposer:
    """
    Application Composer.
    """
    def __init__(self) -> None:
        """
        Constructor.
        """
        self._logger = getLogger(__name__)
        self._logger.info('creating Qt app')
        self._app = QApplication(sys.argv)
        self._logger.debug('creating UI')
        self._mainWindow = MainWindow()

    def run(self):
        """
        Run the application.
        """
        self._mainWindow.show()
        sys.exit(self._app.exec())
