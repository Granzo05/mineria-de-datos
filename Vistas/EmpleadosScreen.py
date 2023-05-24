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