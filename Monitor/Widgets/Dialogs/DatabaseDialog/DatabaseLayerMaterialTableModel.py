from PySide6.QtCore import (
    QAbstractTableModel,
    QObject,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)
from typing import Any


class DatabaseLayerMaterialTableModel(QAbstractTableModel):
    def __init__(self, reopt, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.materials = None

        if not reopt is None:
            self.__fillData(reopt)

    def __fillData(self, reopt):
        if not reopt.abbr2material is None:
            self.materials = {
                key: value
                for key, value in reopt.abbr2material.items()
                if not "0" in key
            }

    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        if self.materials is None:
            return 0
        return len(self.materials)

    def columnCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return 2

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if not index.isValid() or self.materials is None:
            return None

        match role:
            case Qt.ItemDataRole.DisplayRole:
                material = list(self.materials.values())[index.row()]
                match index.column():
                    case 0:
                        return material.airName

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
