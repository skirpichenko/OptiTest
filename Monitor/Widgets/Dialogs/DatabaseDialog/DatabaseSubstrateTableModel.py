from PySide6.QtCore import (
    QAbstractTableModel,
    QObject,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)
from typing import Any


class DatabaseSubstrateTableModel(QAbstractTableModel):
    def __init__(self, reopt, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.chips = None

        if not reopt is None:
            self.__fillData(reopt)

    def __fillData(self, reopt):
        self.chips = reopt.name2chip

    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        if self.chips is None:
            return 0
        return len(self.chips)

    def columnCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return 2

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if not index.isValid() or self.chips is None:
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            chip = list(self.chips.values())[index.row()]
            match index.column():
                case 0:
                    return chip.substrate.material.airName
                
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
                return "Name"
            elif section == 1:
                return "Created at"
        return super().headerData(section, orientation, role)
