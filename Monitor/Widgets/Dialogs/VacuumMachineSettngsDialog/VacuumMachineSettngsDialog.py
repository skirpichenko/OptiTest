from PySide6.QtWidgets import QDialog, QWidget
from UI.VacuumMachineSettngsDialog_ui import Ui_VacuumMachineSettngsDialog


class VacuumMachineSettngsDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_VacuumMachineSettngsDialog()
        self.ui.setupUi(self)
