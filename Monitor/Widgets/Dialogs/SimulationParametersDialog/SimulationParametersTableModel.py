from PySide6.QtCore import (
    QAbstractTableModel,
    QObject,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)
from typing import Any


class SimulationParametersTableModel(QAbstractTableModel):
    def __init__(self, vdp, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.materials = None
        self.depModels = None

        if not vdp is None:
            self.__fillData(vdp)

    def __fillData(self, vdp):
        if not vdp.abbr2material is None and not vdp.abbr2depModel is None:
            # Extract a subset of the dictionary based on a condition
            self.materials = {
                key: value
                for key, value in vdp.abbr2material.items()
                if key in vdp.abbr2depModel.keys()
            }
            self.depModels = vdp.abbr2depModel

    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        if self.materials is None or self.depModels is None:
            return 0

        return len(self.materials)

    def columnCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return 4

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if not index.isValid() or self.materials is None or self.depModels is None:
            return None

        key = list(self.materials.keys())[index.row()]
        match role:
            case Qt.ItemDataRole.DisplayRole:
                match index.column():
                    case 0:
                        return self.materials[key].airName
                    case 1:
                        return str("{:.3f}").format(self.depModels[key].mean)
                    case 2:
                        return str("{:.3f}").format(self.depModels[key].std)
                    case 3:
                        return str("{:.3f}").format(self.depModels[key].meanTime)
            case Qt.ItemDataRole.TextAlignmentRole:
                if index.column() > 0:
                    return Qt.AlignmentFlag.AlignCenter
            case Qt.ItemDataRole.EditRole:
                match index.column():
                    case 1:
                        return self.depModels[key].mean
                    case 2:
                        return self.depModels[key].std
                    case 3:
                        return self.depModels[key].meanTime
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
                return "Material name"
            elif section == 1:
                return "Mean rate, A/s"
            elif section == 2:
                return "RMS, A/s"
            elif section == 3:
                return "Fluct. corr. time"
        return super().headerData(section, orientation, role)

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        if not index.isValid() or self.materials is None or self.depModels is None:
            return Qt.ItemFlag.NoItemFlags

        f = super().flags(index)
        match index.column():
            case 1:
                f |= Qt.ItemFlag.ItemIsEditable
            case 2:
                f |= Qt.ItemFlag.ItemIsEditable
            case 3:
                f |= Qt.ItemFlag.ItemIsEditable
        return f

    def setData(
        self,
        index: QModelIndex | QPersistentModelIndex,
        value: Any,
        role: int = Qt.ItemDataRole.EditRole,
    ) -> bool:
        if not index.isValid() or self.materials is None or self.depModels is None:
            return False

        match role:
            case Qt.ItemDataRole.EditRole:
                key = list(self.materials.keys())[index.row()]
                match index.column():
                    case 1:
                        self.depModels[key].mean = value
                        self.dataChanged.emit(index, index)
                        return True
                    case 2:
                        self.depModels[key].std = value
                        self.dataChanged.emit(index, index)
                        return True
                    case 3:
                        self.depModels[key].meanTime = value
                        self.dataChanged.emit(index, index)
                        return True

        return False
