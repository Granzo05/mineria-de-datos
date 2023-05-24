import datetime

from PyQt5 import QtWidgets, uic, QtCore, Qt
from PyQt5.QtCore import QDate

from Database.EmpleadosDatabase import EmpleadosDatabase
from Vistas.ResultadosBusqueda import ResultadosBusqueda


class EmpleadosScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(EmpleadosScreen, self).__init__()
        uic.loadUi("Interfaz/menu.ui", self)

        # Conectar señales
        self.cargar.clicked.connect(self.cargar_empleado)
        self.buscarDatos.clicked.connect(self.buscar_datos_empleado)
        self.buscarRendimiento.clicked.connect(self.buscar_rendimiento_empleado)
        self.cerrarSesion.clicked.connect(self.cerrar_sesion)

    def cargar_empleado(self):
        try:
            nombre = self.nombreEmpleado.text()
            apellido = self.apellidoEmpleado.text()
            cargo = self.cargoEmpleado.text()
            turno = self.turnoEmpleado.text()

            empleados_database = EmpleadosDatabase()
            empleados_database.agregar_empleado(nombre, apellido, cargo, turno)
            print("Empleado cargado correctamente.")
        except Exception as e:
            self.errorEmpleado.setText("Error al agregar el empleado")
            self.errorEmpleado.show()
            # Configurar el temporizador para ocultar el label después de 2 segundos
            timer = QtCore.QTimer(self)
            timer.singleShot(2000, self.errorEmpleado.hide)
            print("Error al agregar el empleado:", str(e))

    def buscar_datos_empleado(self):
        try:
            id = self.idEmpleado.text()
            nombre = self.nombreEmpleado.text()
            apellido = self.apellidoEmpleado.text()
            cargo = self.cargoEmpleado.text()
            turno = self.turnoEmpleado.text()

            empleados_database = EmpleadosDatabase()
            resultados = empleados_database.buscar_datos_empleado(id, nombre, apellido, cargo, turno)

            resultados_window = ResultadosBusqueda(resultados, "datos_empleado")
            resultados_window.exec_()
        except Exception as e:
            self.errorEmpleado.setText("Error al buscar los datos del empleado")
            self.errorEmpleado.show()
            # Configurar el temporizador para ocultar el label después de 2 segundos
            timer = QtCore.QTimer(self)
            timer.singleShot(2000, self.errorEmpleado.hide)
            print("Error al buscar los datos del empleado:", str(e))

    def buscar_rendimiento_empleado(self):
        try:
            id = self.idEmpleado.text()
            fecha_input = self.fechaEmpleado.text()

            # Convertir la fecha en formato "dd/MM/yyyy" a objeto QDate
            fecha_qdate = QDate.fromString(fecha_input, "dd/MM/yyyy")

            if fecha_qdate.isValid() and fecha_qdate.dayOfWeek() != 7:
                # Obtener la fecha en formato "yyyy-MM-dd"
                fecha_formateada = fecha_qdate.toString("yyyy-MM-dd")
                fecha_formateada = fecha_formateada.replace("/", "-")

                empleados_database = EmpleadosDatabase()
                resultados = empleados_database.buscar_rendimiento_empleado(id, fecha_formateada)
                resultados_window = ResultadosBusqueda(resultados, "rendimiento")
                resultados_window.exec_()
            else:
                self.errorEmpleado.setText(fecha_input + " no fue un día laboral")
                self.errorEmpleado.show()
                # Configurar el temporizador para ocultar el label después de 2 segundos
                timer = QtCore.QTimer(self)
                timer.singleShot(2000, self.errorEmpleado.hide)
        except Exception as e:
            self.errorEmpleado.setText("Error al buscar el rendimiento del empleado")
            self.errorEmpleado.show()
            # Configurar el temporizador para ocultar el label después de 2 segundos
            timer = QtCore.QTimer(self)
            timer.singleShot(2000, self.errorEmpleado.hide)
            print("Error al buscar el rendimiento del empleado:", str(e))

    def cerrar_sesion(self):
        try:
            self.close()
        except Exception as e:
            print("Error al cerrar la sesión:", str(e))
