from PySide6.QtWidgets import QDialog, QWidget
from UI.ProjectsDialog_ui import Ui_ProjectsDialog
from Widgets.Dialogs.ProjectsDialog.ProjectsListModel import ProjectsListModel

class ProjectsDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_ProjectsDialog()
        self.ui.setupUi(self)

        self.model = ProjectsListModel()
        self.ui.listViewProjects.setModel(self.model)
