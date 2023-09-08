from PySide6.QtWidgets import QDialog, QWidget
from UI.HistoryDialog_ui import Ui_HistoryDialog
from Widgets.Dialogs.HistoryDialog.HistoryListModel import HistoryListModel


class HistoryDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_HistoryDialog()
        self.ui.setupUi(self)

        self.model = HistoryListModel()
        self.ui.listViewHistory.setModel(self.model)
