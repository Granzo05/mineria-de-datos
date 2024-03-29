from PyQt5 import QtWidgets, uic

from Vistas.AgregarEmpleado import AgregarEmpleado
from Vistas.EmpleadosScreen import EmpleadosScreen


class Menu(QtWidgets.QMainWindow):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Menu, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super(Menu, self).__init__()
        uic.loadUi("Interfaz/menu.ui", self)

        self.agregar.clicked.connect(self.agregar_screen)
        self.salir.clicked.connect(self.salir_screen)
        self.cerrarSesion.clicked.connect(self.cerrar_sesion)
        self.buscar.clicked.connect(self.buscar_screen)

    def buscar_screen(self):
        try:
            self.hide()
            window = EmpleadosScreen()
            window.show()
        except Exception as e:
            print(f"Error al abrir la ventana: {str(e)}")

    def agregar_screen(self):
        try:
            self.hide()
            window = AgregarEmpleado()
            window.show()
        except Exception as e:
            print(f"Error al abrir la ventana: {str(e)}")

    def salir_screen(self):
        self.close()

    def cerrar_sesion(self):
        try:
            from Vistas.LoginScreen import LoginScreen
            login_screen = LoginScreen()
            login_screen.show()
            self.close()
        except Exception as e:
            print(f"Error al abrir la ventana: {str(e)}")
