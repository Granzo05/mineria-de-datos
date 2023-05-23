from PyQt5 import uic, QtWidgets

from Database.EmpleadosDatabase import EmpleadosDatabase
from Vistas.EmpleadosScreen import EmpleadosScreen


class LoginScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginScreen, self).__init__()
        self.window2 = None
        uic.loadUi("Interfaz/login.ui", self)

        # Conectar señales
        self.iniciaSesion.clicked.connect(self.buscar_usuario_login)
        self.salir.clicked.connect(self.salir_click)

        self.usuario_contra_inc.setVisible(False)

    def buscar_usuario_login(self):
        nombre = self.usuarioJefe.text()
        contrasenia = self.contraJefe.text()

        empleados_data = EmpleadosDatabase()

        if empleados_data.buscar_usuario(nombre, contrasenia):
            print("Inicio de sesión exitoso")
            self.abrir_menu_empleados()
        else:
            self.usuario_contra_inc.setVisible(True)
            print("Usuario o contraseña incorrectos")

    def salir_click(self):
        self.close()

    def abrir_menu_empleados(self):
        self.hide()
        self.window2 = EmpleadosScreen()
        self.window2.show()
