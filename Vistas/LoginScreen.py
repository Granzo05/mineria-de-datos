import random
import time

from PyQt5 import uic, QtWidgets
from Database.EmpleadosDatabase import EmpleadosDatabase


class LoginScreen(QtWidgets.QMainWindow):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoginScreen, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super(LoginScreen, self).__init__()
        uic.loadUi("Interfaz/login.ui", self)

        # Conectar señales
        self.barraInicio.setVisible(False)
        self.iniciando.setVisible(False)
        self.iniciaSesion.clicked.connect(self.buscar_usuario_login)
        self.salir.clicked.connect(self.salir_click)

        self.usuario_contra_inc.setVisible(False)

        # Usuario: test
        # Contraseña: test

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
                self.repaint()
                time.sleep(0.5)
                self.usuario_contra_inc.setVisible(False)
                self.repaint()

    def salir_click(self):
        self.close()

    def abrir_menu(self):
        try:
            from Vistas.Menu import Menu
            menu_screen = Menu()
            menu_screen.show()
            self.close()
        except Exception as e:
            print(f"Error al abrir la ventana: {str(e)}")

    def simulacion_carga(self):
        self.barraInicio.setVisible(True)
        self.barraInicio.setMinimum(0)
        self.barraInicio.setMaximum(100)
        self.barraInicio.setTextVisible(False)

        style_sheet = """
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                background-color: #f0f0f0;
                min-width: 275px;
            }

            QProgressBar::chunk {
                background-color: #2196F3;
                width: 20px;
            }
        """
        self.barraInicio.setStyleSheet(style_sheet)

        valor = 0
        while valor <= 100:

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
