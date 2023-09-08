from PySide6.QtCore import (
    QAbstractTableModel,
    QObject,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)
from typing import Any


class DatabaseRefractiveIndexTableModel(QAbstractTableModel):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.refractive_index = None

    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        if self.refractive_index is None:
            return 0
        return len(self.refractive_index.wavelength)

    def columnCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return 3

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if (
            index.isValid()
            and role == Qt.ItemDataRole.DisplayRole
            and self.refractive_index is not None
        ):
            match index.column():
                case 0:
                    return str(self.refractive_index.wavelength[index.row()])
                case 1:
                    return str(self.refractive_index.n[index.row()])
                case 2:
                    return str(self.refractive_index.k[index.row()])
        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            if section == 0:
                return "wavelength"
            elif section == 1:
                return "n"
            elif section == 2:
                return "k"
        return super().headerData(section, orientation, role)

    def set_refractive_index(self, refractive_index):
        self.beginResetModel()
        self.refractive_index = refractive_index
        self.endResetModel()
