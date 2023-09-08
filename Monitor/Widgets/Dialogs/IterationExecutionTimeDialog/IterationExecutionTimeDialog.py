from PySide6.QtWidgets import QDialog, QWidget
from UI.IterationExecutionTimeDialog_ui import Ui_IterationExecutionTimeDialog
from Widgets.Dialogs.IterationExecutionTimeDialog.IterationExecutionTimeListModel import (
    IterationExecutionTimeListModel,
)


class IterationExecutionTimeDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_IterationExecutionTimeDialog()
        self.ui.setupUi(self)

        self.model = IterationExecutionTimeListModel()
        self.ui.listViewIterationExecTime.setModel(self.model)
