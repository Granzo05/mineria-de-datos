from PyQt5 import QtWidgets, uic

from Vistas.AgregarEmpleado import AgregarEmpleado
from Vistas.EmpleadosScreen import EmpleadosScreen


class MainMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainMenu, self).__init__()
        uic.loadUi("Interfaz/menu.ui", self)

        # Acceso a los botones
        self.agregar.clicked.connect(self.agregar_screen)
        self.salir.clicked.connect(self.salir_screen)
        self.cerrarSesion.clicked.connect(self.cerrar_sesion)
        self.buscar.clicked.connect(self.buscar_screen)

    def buscar_screen(self):
        self.hide()
        window = EmpleadosScreen()
        window.show()

    def agregar_screen(self):
        self.hide()
        window = AgregarEmpleado()
        window.show()

    def salir_screen(self):
        self.close()

    def cerrar_sesion(self):
        from Vistas.LoginScreen import LoginScreen
        login_screen = LoginScreen()
        login_screen.show()
        self.close()
