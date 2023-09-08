from PySide6.QtCore import Qt, QAbstractItemModel, QModelIndex, QPersistentModelIndex
from PySide6.QtWidgets import (
    QStyleOptionViewItem,
    QWidget,
    QStyledItemDelegate,
    QDoubleSpinBox,
)
from PySide6.QtCore import QObject
import typing
import sys


class SimulationParametersDoubleDelegate(QStyledItemDelegate):
    def __init__(self, parent: typing.Optional[QObject] = None) -> None:
        super().__init__(parent)

    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:
        sb = QDoubleSpinBox(parent)
        sb.setDecimals(3)
        match index.column():
            case 3:
                sb.setRange(sys.float_info.min, sys.float_info.max)
            case _:
                sb.setRange(0, sys.float_info.max)
        return sb

    def setEditorData(
        self, editor: QWidget, index: QModelIndex | QPersistentModelIndex
    ) -> None:
        if isinstance(editor, QDoubleSpinBox):
            editor.setValue(index.data(Qt.ItemDataRole.EditRole))
        return super().setEditorData(editor, index)

    def setModelData(
        self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex
    ) -> None:
        if isinstance(editor, QDoubleSpinBox):
            model.setData(index, editor.value(), Qt.ItemDataRole.EditRole)
        else:
            super().setModelData(editor, model, index)

    def updateEditorGeometry(
        self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        super().updateEditorGeometry(editor, option, index)
        editor.setGeometry(option.rect.adjusted(0, 0, 0, -1))
