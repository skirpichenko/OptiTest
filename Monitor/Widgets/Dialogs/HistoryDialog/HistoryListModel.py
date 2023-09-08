from PySide6.QtCore import (
    QAbstractListModel,
    QObject,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)
from typing import Any


class HistoryListModel(QAbstractListModel):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return 5

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            return f"History {index.row() + 1}"
        return None