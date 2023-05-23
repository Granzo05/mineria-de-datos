from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableWidgetItem


class ResultadosBusqueda(QDialog):
    def __init__(self, resultados):
        super(ResultadosBusqueda, self).__init__()
        uic.loadUi("Interfaz/tabla.ui", self)

        # Configurar la tabla con los resultados de la búsqueda
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "FECHA", "ASISTENCIA", "PASOS", "VENTAS", "NIVEL DE ESTRÉS", "ID EMPLEADO"])
        self.tableWidget.setRowCount(len(resultados))

        for row, resultado in enumerate(resultados):
            for col, valor in enumerate(resultado):
                item = QTableWidgetItem(str(valor))
                self.tableWidget.setItem(row, col, item)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tableWidget.resizeColumnsToContents()