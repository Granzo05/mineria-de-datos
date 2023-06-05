
from PyQt5 import QtWidgets, uic

from Database.EmpleadosDatabase import EmpleadosDatabase


class AgregarEmpleado(QtWidgets.QMainWindow):
    def __init__(self):
        super(AgregarEmpleado, self).__init__()
        uic.loadUi("Interfaz/add.ui", self)

        nombre = self.nombreEmpleado.text()
        apellido = self.apellidoEmpleado.text()
        cargo = self.cargoEmpleado.text()
        turno = self.turnoEmpleado.text()

        with EmpleadosDatabase() as empleados_data:
            self.anadirEmpleado.clicked.connect(
                lambda: empleados_data.agregar_empleado(nombre, apellido, cargo, turno, self.errorEmpleado)
            )
            self.salir.clicked.connect(self.salir_click)
            self.cerrarSesion.clicked.connect(self.cerrar_sesion)
            self.volver.clicked.connect(self.volver_click)

    def cerrar_sesion(self):
        from Vistas.LoginScreen import LoginScreen
        login_screen = LoginScreen()
        login_screen.show()
        self.close()

    def salir_click(self):
        self.close()

    def volver_click(self):
        from Vistas.Menu import Menu
        menu_screen = Menu()
        menu_screen.show()
        self.close()
