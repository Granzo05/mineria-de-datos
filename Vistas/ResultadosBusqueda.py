from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableWidgetItem


class ResultadosBusqueda(QDialog):
    def __init__(self, resultados):
        super(ResultadosBusqueda, self).__init__()
        uic.loadUi("Interfaz/tabla.ui", self)

        print(resultados)
        # Establecer las columnas a mostrar en la tabla
        columnas = ["ID", "FECHA", "PASOS", "HORAS DE TRABAJO", "ASISTENCIA", "NIVEL DE ESTRÉS", "ID EMPLEADO"]

        self.tableWidget.setColumnCount(len(columnas))
        self.tableWidget.setHorizontalHeaderLabels(columnas)

        # Calcular la cantidad de filas necesarias para mostrar los resultados
        num_rows = len(resultados)

        # Establecer la cantidad de filas en la tabla
        self.tableWidget.setRowCount(num_rows)

        for row, resultado in enumerate(resultados):
            for col, valor in enumerate(resultado):
                item = QTableWidgetItem(str(valor))
                self.tableWidget.setItem(row, col, item)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tableWidget.resizeColumnsToContents()