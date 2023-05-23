from PyQt5 import QtWidgets, uic

from Database.EmpleadosDatabase import EmpleadosDatabase
from Vistas.ResultadosBusqueda import ResultadosBusqueda


class EmpleadosScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(EmpleadosScreen, self).__init__()
        uic.loadUi("Interfaz/menu.ui", self)

        # Conectar señales
        self.cargar.clicked.connect(self.cargar_empleado)
        #Todo: Crear estos botones:
        # self.buscar_datos_empleado.clicked.connect(self.buscar_datos_empleado)
        # self.buscar_rendimiento_empleado.clicked.connect(self.buscar_rendimiento_empleado)
        self.cerrarSesion.clicked.connect(self.cerrar_sesion)

    def cargar_empleado(self):
        nombre = self.nombreEmpleado.text()
        apellido = self.apellidoEmpleado.text()
        #Todo: Crear estos campos
        # cargo = self.cargoEmpleado.text()
        # turno = self.turnoEmpleado.text()

        empleados_database = EmpleadosDatabase()
        empleados_database.agregar_empleado(nombre, apellido, cargo, turno)

    def buscar_datos_empleado(self):
        id = self.idEmpleado.text()
        nombre = self.nombreEmpleado.text()
        apellido = self.apellidoEmpleado.text()
        #Todo: Crear estos campos
        # cargo = self.cargoEmpleado.text()
        # turno = self.turnoEmpleado.text()

        empleados_database = EmpleadosDatabase()
        resultados = empleados_database.buscar_datos_empleado(id, nombre, apellido, cargo, turno)

        resultados_window = ResultadosBusqueda(resultados, "datos_empleado")
        resultados_window.exec_()

    def buscar_rendimiento_empleado(self):
        id = self.idEmpleado.text()
        #Todo: Crear este campo
        # fecha = self.fechaBuscada.text()

        empleados_database = EmpleadosDatabase()
        resultados = empleados_database.buscar_parametros_empleado(id, fecha)

        resultados_window = ResultadosBusqueda(resultados, "rendimiento")
        resultados_window.exec_()

    def cerrar_sesion(self):
        self.close()
