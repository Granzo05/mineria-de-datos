from PyQt5 import QtWidgets, uic

from Database.EmpleadosDatabase import EmpleadosDatabase


class EmpleadosScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(EmpleadosScreen, self).__init__()
        uic.loadUi("Interfaz/menu.ui", self)

        # Conectar señales
        self.cargar.clicked.connect(self.cargar_empleado)
        self.buscar.clicked.connect(self.buscar_empleado)
        self.cerrarSesion.clicked.connect(self.cerrar_sesion)

    def cargar_empleado(self):
        empleados_database = EmpleadosDatabase()
        nombre = self.nombreEmpleado.text()
        apellido = self.apellidoEmpleado.text()
        cargo = self.cargoEmpleado.text()
        turno = self.turnoEmpleado.text()

        # Lógica para guardar el empleado en la base de datos
        empleados_database.guardar_empleado(nombre, apellido, cargo, turno)

    def buscar_empleado(self):
        empleados_database = EmpleadosDatabase()
        nombre = self.nombreEmpleado.text()
        apellido = self.apellidoEmpleado.text()
        cargo = self.cargoEmpleado.text()
        turno = self.turnoEmpleado.text()

        # Realiza la lógica para buscar el empleado en la otra clase
        resultados = empleados_database.buscar_empleado(nombre, apellido, cargo, turno)


    def cerrar_sesion(self):
        self.close()
