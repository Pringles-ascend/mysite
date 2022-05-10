import pandas as pd
import numpy as np

from PySide6.QtWidgets import QTableView, QApplication
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QTimer
import sys


class PandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(2000)

    def tick(self):
        self._dataframe = pd.DataFrame(np.random.randint(10,100,16).reshape(4,4),columns=list('abcd'))
        self._dataframe = self._dataframe.set_index('a')
        # index_1 = self.index(0, 0)
        
        # index_2 = self.index(10, 5)
        self.dataChanged.emit(self.index(0,100), [Qt.DisplayRole])
        # self.dataChanged.emit(1,1,1)

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])

        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])

        return None


if __name__ == "__main__":

    app = QApplication(sys.argv)

    df = pd.DataFrame(np.random.randint(10,100,16).reshape(4,4),columns=list('abcd'))
    df = df.set_index('a')

    view = QTableView()
    view.resize(800, 500)
    view.horizontalHeader().setStretchLastSection(True)
    view.verticalHeader().hide()
    view.setAlternatingRowColors(True)
    view.setSelectionBehavior(QTableView.SelectRows)

    model = PandasModel(df)
    view.setModel(model)
    view.show()
    app.exec()