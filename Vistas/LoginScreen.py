import random
import sys
import time

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QCoreApplication
from Database.EmpleadosDatabase import EmpleadosDatabase


class LoginScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginScreen, self).__init__()
        uic.loadUi("Interfaz/login.ui", self)

        # Conectar señales
        self.barraInicio.setVisible(False)
        self.iniciando.setVisible(False)
        self.iniciaSesion.clicked.connect(self.buscar_usuario_login)
        self.salir.clicked.connect(self.salir_click)

        self.usuario_contra_inc.setVisible(False)

    def buscar_usuario_login(self):
        nombre = self.usuarioJefe.text()
        contrasenia = self.contraJefe.text()

        with EmpleadosDatabase() as empleados_data:
            if empleados_data.buscar_usuario(nombre, contrasenia):
                self.iniciando.setVisible(True)
                self.simulacion_carga()
                self.abrir_menu()
            else:
                self.usuario_contra_inc.setVisible(True)
                print("Usuario o contraseña incorrectos")

    def salir_click(self):
        self.close()

    def abrir_menu(self):
        try:
            app = QtWidgets.QApplication(sys.argv)
            login_screen = LoginScreen()
            login_screen.show()
            sys.exit(app.exec_())
        except Exception as e:
            print(f"Error al abrir la ventana: {str(e)}")

    def simulacion_carga(self):
        self.barraInicio.setVisible(True)
        valor = 0  # Valor inicial del progreso
        while valor <= 100:
            print("Progreso:", valor, "%")

            # Simular tiempo de espera
            time.sleep(0.01)

            probabilidad = random.randint(1, 100)

            if probabilidad <= 45:
                avance = 2
            elif probabilidad <= 30:
                avance = 3
            elif probabilidad <= 15:
                avance = 4
            else:
                avance = 1

            # Actualizar el progreso según la probabilidad de avance
            valor += avance
            self.barraInicio.setValue(valor)