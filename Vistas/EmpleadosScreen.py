
from PyQt5 import QtWidgets



class EmpleadosScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(EmpleadosScreen, self).__init__()
        uic.loadUi("Interfaz/search.ui", self)

        self.volver.clicked.connect(lambda: self.volver_screen())
        self.salir.clicked.connect(self.salir_screen)
        self.cerrarSesion.clicked.connect(self.cerrar_sesion)

        self.filtroNombre = QtWidgets.QCheckBox()
        self.filtroApellido = QtWidgets.QCheckBox()
        self.filtroCargo = QtWidgets.QCheckBox()
        self.filtroTurno = QtWidgets.QCheckBox()
        self.filtros = QtWidgets.QCheckBox()

        self.buscarRendimiento.clicked.connect(self.buscar_rendimiento_empleado)

        with EmpleadosDatabase() as empleados_data:
            empleados_data.obtener_empleados(self.tablaDatos)

    def cerrar_sesion(self):
        try:
            self.close()
        except Exception as e:
            print("Error al cerrar la sesión:", str(e))

    def salir_screen(self):
        self.close()

    def volver_screen(self):
        from Vistas.Menu import Menu
        menu_screen = Menu()
        menu_screen.show()
        self.close()

    def cerrar_sesion(self):
        from Vistas.LoginScreen import LoginScreen
        login_screen = LoginScreen()
        login_screen.show()
        self.close()

    def buscar_rendimiento_empleado(self):
        nombre = self.buscarNombre.text()
        apellido = self.buscarApellido.text()
        idEmpleado = self.buscarId.text()
        cargo = self.buscarCargo.text()
        turno = self.buscarTurno.text()
        idRendimiento = self.idRendimiento.text()
        fecha_input = self.fechaRendimiento.text()

        with EmpleadosDatabase() as empleados_data:
            empleados_data.buscar_rendimiento_empleado(nombre, apellido, cargo, turno, idRendimiento, fecha_input,
                                                       idEmpleado)

from PyQt5 import QtWidgets, uic

from Database.EmpleadosDatabase import EmpleadosDatabase


class EmpleadosScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(EmpleadosScreen, self).__init__()
        uic.loadUi("Interfaz/search.ui", self)

        id = self.idEmpleado.text()
        nombre = self.nombreEmpleado.text()
        apellido = self.apellidoEmpleado.text()
        cargo = self.cargoEmpleado.text()
        turno = self.turnoEmpleado.text()
        fecha_input = self.fechaEmpleado.text()

        with EmpleadosDatabase() as empleados_data:
            self.cargar.clicked.connect(
                lambda: empleados_data.agregar_empleado(nombre, apellido, cargo, turno, self.errorEmpleado)
            )
            self.buscarDatos.clicked.connect(
                lambda: empleados_data.buscar_datos_empleado(id, nombre, apellido, cargo, turno, self.errorEmpleado)
            )
            self.buscarRendimiento.clicked.connect(
                lambda: empleados_data.buscar_rendimiento_empleado(id, fecha_input, self.errorEmpleado)
            )
            self.cerrarSesion.clicked.connect(self.cerrar_sesion)

            # Resto del código que utiliza empleados_data

            empleados_data.close_connection()  # Cerrar la conexión y el cursor después de utilizarlos

    def cerrar_sesion(self):
        try:
            self.close()
        except Exception as e:
            print("Error al cerrar la sesión:", str(e))

