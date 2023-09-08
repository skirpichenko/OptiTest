from PySide6.QtCore import (
    QAbstractTableModel,
    QObject,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)
from typing import Any


class DatabaseDesignTableModel(QAbstractTableModel):
    def __init__(self, reopt, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.phThicknesses = None
        self.qwotThicknesses = None
        self.materialNames = None

        if not reopt is None:
            self.__fillData(reopt)

    def __fillData(self, reopt):
        design = reopt.design
        if not reopt.design is None:
            self.phThicknesses = design.ph_thicknesses
            self.qwotThicknesses = design.qwot_thicknesses
            self.materialNames = [layer.material.airName for layer in design.layers]

    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        if (
            self.phThicknesses is None
            or self.qwotThicknesses is None
            or self.materialNames is None
        ):
            return 0
        return len(self.phThicknesses)

    def columnCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return 5

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if (
            not index.isValid()
            or self.phThicknesses is None
            or self.qwotThicknesses is None
            or self.materialNames is None
        ):
            return None

        match role:
            case Qt.ItemDataRole.DisplayRole:
                row = index.row()
                match index.column():
                    case 0:
                        return str("{:.2f}").format(self.phThicknesses[row])
                    case 1:
                        return str("{:.2f}").format(self.qwotThicknesses[row])
                    case 2:
                        return str(self.materialNames[row])
            case Qt.ItemDataRole.TextAlignmentRole:
                return Qt.AlignmentFlag.AlignCenter

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
                return "Physical th"
            elif section == 1:
                return "QWOT"
            elif section == 2:
                return "Material"
            elif section == 3:
                return "Thickness control "
            elif section == 4:
                return "Time (sec)"
        return super().headerData(section, orientation, role)
