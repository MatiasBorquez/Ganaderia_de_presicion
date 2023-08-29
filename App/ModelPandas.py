import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

import TratamientoCSV
import pandas as pd

#  Crear un modelo de tabla a partir de un DataFrame de Pandas,
#  lo que permite mostrar los datos del DataFrame en una vista de tabla en una interfaz gráfica de usuario.
class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df, parent=None):
        # llama al método __init__ de la clase base QAbstractTableModel para inicializar correctamente el objeto.
        # Se pasa el argumento parent al constructor de la clase base.
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        # Este atributo se utilizará en otros métodos de la clase para acceder a los datos del DataFrame.
        self._df = df

    #  Este método se utiliza para proporcionar los datos de los encabezados de las filas y columnas de la tabla.
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        #  Verifica si el valor del argumento role es diferente de QtCore.Qt.DisplayRole.
        #  Si es así, el método devuelve un objeto vacío de tipo QtCore.QVariant.
        #  Esto indica que no se proporciona ningún dato para roles diferentes a DisplayRole.
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        # Verifica si el valor del argumento orientation es igual a QtCore.Qt.Horizontal.
        # Si es así, el método intenta devolver el nombre de la columna correspondiente al índice especificado por el argumento section.
        # Si ocurre un error de índice al intentar acceder al nombre de la columna, el método devuelve un objeto vacío de tipo QtCore.QVariant.
        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

        # Verifica si el valor del argumento orientation es igual a QtCore.Qt.Vertical.
        # Si es así, el método intenta devolver el nombre del índice correspondiente al índice especificado por el argumento section.
        # Si ocurre un error de índice al intentar acceder al nombre del índice, el método devuelve un objeto vacío de tipo QtCore.QVariant.
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    #  Este método se utiliza para proporcionar los datos para cada celda de la tabla
    def data(self, index, role=QtCore.Qt.DisplayRole):
        # verifican si el valor del argumento role es diferente de QtCore.Qt.DisplayRole.
        # Si es así, el método devuelve un objeto vacío de tipo QtCore.QVariant.
        # Esto indica que no se proporciona ningún dato para roles diferentes a DisplayRole.
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        # verifican si el objeto QModelIndex proporcionado como argumento index es válido
        if not index.isValid():
            return QtCore.QVariant()

        # devuelve el dato correspondiente a la celda especificada por el objeto QModelIndex proporcionado como argumento index.
        #  El dato se convierte a una cadena y se devuelve como un objeto QtCore.QVariant.
        return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))

    # Este método se utiliza para modificar los datos del modelo.
    # index, que es un objeto QModelIndex que especifica la fila y columna de la celda a modificar;
    # value, que es el nuevo valor para la celda; y role, que indica el tipo de dato a modificar.
    def setData(self, index, value, role):
        #  Obtiengo los nombres del índice y de la columna correspondientes a la celda especificada por el objeto QModelIndex proporcionado como argumento index.
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        # Verifica si el objeto value proporcionado como argumento tiene un método llamado toPyObject.
        # Si es así, se asume que el objeto es un QVariant y se llama al método toPyObject para obtener el valor subyacente.
        # De lo contrario, se asume que el objeto es una cadena Unicode y se verifica si el tipo de datos de la columna especificada es diferente de object.
        # Si es así, se convierte el valor a ese tipo de datos utilizando el método type del tipo de datos.
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        # El método set_value del DataFrame para modificar el valor en la fila y columna especificadas por los nombres del índice y de la columna.
        self._df.set_value(row, col, value)
        # devuelve True para indicar que la operación fue exitosa.
        return True

    # Este método se utiliza para obtener el número de filas en el modelo.
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    #  Este método se utiliza para obtener el número de columnas en el modelo
    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    '''def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()'''