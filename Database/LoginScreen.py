from PyQt5 import uic
from PyQt5.uic.properties import QtWidgets

from EmpleadosScreen import EmpleadosScreen


class login_screen(QtWidgets.QMainWindow):
    def __init__(self, empleados_data):
        super(login_screen, self).__init__()
        uic.loadUi("login.ui", self)

        self.empleados_data = empleados_data

        # Conectar señales y slots
        self.iniciaSesion.clicked.connect(self.buscar_usuario_login)
        self.salir.clicked.connect(self.salir_click)

        # Ocultar el QLabel "usuario_contra_inc" inicialmente
        self.usuario_contra_inc.setVisible(False)

    def buscar_usuario_login(self):
        nombre = self.usuarioJefe.text()
        contrasenia = self.contraJefe.text()

        resultados = self.empleados_data.buscar_usuario(nombre, contrasenia)

        if resultados is None:
            self.usuario_contra_inc.setVisible(True)
        else:
            self.abrir_menu_empleados()

    def salir_click(self):
        self.close()

    def abrir_menu_empleados(self):
        self.hide()
        window2 = EmpleadosScreen(self.empleados_data)
        window2.show()
