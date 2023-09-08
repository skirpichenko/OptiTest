import path_config
from PySide6.QtWidgets import QApplication
import sys
from MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("Optilayer")
    app.setApplicationName("Monitor")

    w = MainWindow()
    w.show()

    sys.exit(app.exec())
