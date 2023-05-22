from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic.properties import QtWidgets

from EmpleadosDatabase import EmpleadosDatabase
from ResultadosBusqueda import ResultadosBusqueda


class EmpleadosScreen(QtWidgets.QMainWindow):
    def __init__(self, empleados_data):
        super(EmpleadosScreen, self).__init__()
        uic.loadUi("menuEmpleados.ui", self)

        self.empleados_data = empleados_data

        # Conectar señales y slots
        self.ui.cargar.clicked.connect(self.cargar_empleado)
        self.ui.buscar.clicked.connect(self.buscar_empleado)
        self.ui.cerrarSesion.clicked.connect(self.cerrar_sesion)

    def cargar_empleado(self):
        empleados_database = EmpleadosDatabase()
        nombre = self.ui.nombreEmpleado.text()
        apellido = self.ui.apellidoEmpleado.text()
        cargo = self.ui.cargoEmpleado.text()
        turno = self.ui.turnoEmpleado.text()

        if empleados_database.agregar_empleado(nombre, apellido, cargo, turno):
            QMessageBox.information(self, "Cargar Empleado", "El empleado ha sido cargado correctamente.")
        else:
            QMessageBox.warning(self, "Cargar Empleado",
                                "Error al cargar el empleado. Por favor, inténtelo nuevamente.")

    def buscar_empleado(self):
        empleados_database = EmpleadosDatabase()
        nombre = self.ui.nombreEmpleado.text()
        apellido = self.ui.apellidoEmpleado.text()
        cargo = self.ui.cargoEmpleado.text()
        turno = self.ui.turnoEmpleado.text()

        # Realiza la lógica para buscar el empleado en la otra clase
        resultados = empleados_database.buscar_empleado(nombre, apellido, cargo, turno)

        if resultados:
            resultados_dialog = ResultadosBusqueda(resultados)
            resultados_dialog.exec_()
        else:
            QMessageBox.information(self, "Buscar Empleado",
                                    "No se encontraron resultados para los criterios de búsqueda especificados.")

    def cerrar_sesion(self):
        # Realiza la lógica para cerrar la sesión
        # Aquí puedes agregar tu propia implementación

        # Cierra la ventana actual
        self.close()
