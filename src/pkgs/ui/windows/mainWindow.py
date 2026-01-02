"""
Main application window.
"""

from logging import getLogger
from pathlib import Path
from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice


class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()
        self._logger = getLogger(__name__)
        self._logger.info('Initializing main window')
        self._load_ui()
        self._setup_connections()

    def _load_ui(self) -> None:
        """
        Load the UI from the Qt Designer .ui file.
        """
        # Path to the UI file
        ui_file_path = Path(__file__).parent.parent / "designer" / "mainWindow.ui"

        self._logger.debug(f'Loading UI from: {ui_file_path}')

        if not ui_file_path.exists():
            error_msg = f"UI file not found: {ui_file_path}"
            self._logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        # Load the UI file
        ui_file = QFile(str(ui_file_path))
        if not ui_file.open(QIODevice.ReadOnly):
            error_msg = f"Cannot open UI file: {ui_file_path}"
            self._logger.error(error_msg)
            raise IOError(error_msg)

        try:
            loader = QUiLoader()
            # Load with self as parent so widgets belong to this window
            loaded_window = loader.load(ui_file, self)

            if not loaded_window:
                error_msg = f"Failed to load UI from: {ui_file_path}"
                self._logger.error(error_msg)
                raise RuntimeError(error_msg)

            # Copy properties from the loaded window to self
            self.setWindowTitle(loaded_window.windowTitle())
            self.setGeometry(loaded_window.geometry())

            # Get the central widget (which contains the QTabWidget)
            central_widget = loaded_window.centralWidget()
            if central_widget:
                # Reparent the central widget to this window
                central_widget.setParent(self)
                # Set it as our central widget
                self.setCentralWidget(central_widget)

            # Store reference to the central widget to access UI elements
            self._ui = central_widget

            self._logger.debug('UI loaded successfully')

        finally:
            ui_file.close()

    def _setup_connections(self) -> None:
        """
        Set up signal/slot connections.
        This will be expanded later to connect UI elements to calculator logic.
        """
        self._logger.debug('Setting up connections')

        # Access UI elements through self._ui
        # Example: self._ui.folktailTab, self._ui.ironTeethTab, etc.

        # TODO: Set up connections to calculator controllers
        pass
