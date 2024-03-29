from Database.EmpleadosDatabase import EmpleadosDatabase
from PyQt5 import QtWidgets, uic
import time


class AgregarEmpleado(QtWidgets.QMainWindow):
    def __init__(self):
        super(AgregarEmpleado, self).__init__()
        uic.loadUi("Interfaz/add.ui", self)

        self.agregarEmpleado.clicked.connect(
            lambda: self.agregar_empleado()
        )
        self.salir.clicked.connect(self.salir_click)
        self.cerrarSesion.clicked.connect(self.cerrar_sesion)
        self.volver.clicked.connect(self.volver_click)
        self.errorEmpleado.setVisible(False)
        self.addExito.setVisible(False)

    def cerrar_sesion(self):
        try:
            from Vistas.LoginScreen import LoginScreen
            login_screen = LoginScreen()
            login_screen.show()
            self.close()
        except Exception as e:
            print(f"Error al abrir la ventana: {str(e)}")

    def salir_click(self):
        try:
            self.close()
        except Exception as e:
            print("Error al salir:", str(e))

    def volver_click(self):
        try:
            from Vistas.Menu import Menu
            menu_screen = Menu()
            menu_screen.show()
            self.hide()
        except Exception as e:
            print("Error al volver:", str(e))

    def agregar_empleado(self):

        nombre = self.nombreEmpleado.text()
        apellido = self.apellidoEmpleado.text()
        cargo = self.cargoEmpleado.text()
        turno = self.turnoEmpleado.text()

        if nombre and apellido and cargo and turno:
            try:
                with EmpleadosDatabase() as empleados_data:
                    empleados_data.agregar_empleado(nombre, apellido, cargo, turno)

                    self.addExito.setVisible(True)
                    self.nombreEmpleado.setText("")
                    self.apellidoEmpleado.setText("")
                    self.cargoEmpleado.setText("")
                    self.turnoEmpleado.setText("")

                    self.repaint()
                    time.sleep(2)
                    self.addExito.setVisible(False)
                    self.repaint()
            except Exception as e:
                print("Error al agregar empleado:", str(e))
                self.errorEmpleado.setVisible(True)
                self.repaint()
                time.sleep(2)
                self.errorEmpleado.setVisible(False)
                self.repaint()
        else:
            print("Todos los campos deben estar completos.")
            self.errorEmpleado.setVisible(True)
            self.repaint()
            time.sleep(2)
            self.errorEmpleado.setVisible(False)
            self.repaint()