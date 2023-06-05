from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate

from Database.EmpleadosDatabase import EmpleadosDatabase
from Vistas.ResultadosBusqueda import ResultadosBusqueda


class EmpleadosScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(EmpleadosScreen, self).__init__()
        uic.loadUi("Interfaz/search.ui", self)

        self.volver.clicked.connect(lambda: self.volver_screen())
        self.salir.clicked.connect(self.salir_screen)
        self.cerrarSesion.clicked.connect(self.cerrar_sesion)

        self.errorIdFecha.setVisible(False)
        self.buscarNombre.setVisible(False)
        self.buscarApellido.setVisible(False)
        self.buscarCargo.setVisible(False)
        self.buscarTurno.setVisible(False)
        self.filtroNombre.setVisible(False)
        self.filtroApellido.setVisible(False)
        self.filtroCargo.setVisible(False)
        self.filtroTurno.setVisible(False)
        self.filtros.stateChanged.connect(self.actualizarFiltros)

        self.filtroNombre.stateChanged.connect(self.actualizarFiltros)
        self.filtroApellido.stateChanged.connect(self.actualizarFiltros)
        self.filtroCargo.stateChanged.connect(self.actualizarFiltros)
        self.filtroTurno.stateChanged.connect(self.actualizarFiltros)
        self.filtros.stateChanged.connect(self.actualizarFiltros)

        self.buscarRendimiento.clicked.connect(self.buscar_rendimiento_empleado)

        self.buscarNombre.textChanged.connect(self.actualizarFiltroNombre)
        self.buscarApellido.textChanged.connect(self.actualizarFiltroApellido)
        self.buscarCargo.textChanged.connect(self.actualizarFiltroCargo)
        self.buscarTurno.textChanged.connect(self.actualizarFiltroTurno)

        fecha_inicio = QDate(2023, 4, 27)

        self.fechaRendimiento.setDate(fecha_inicio)

        with EmpleadosDatabase() as empleados_data:
            empleados_data.obtener_parametros_empleados(self.tablaDatos)

            empleados_data.traer_empleados(self.tablaEmpleados)

    def salir_screen(self):
        self.close()

    def volver_screen(self):
        from Vistas.Menu import Menu
        menu_screen = Menu()
        menu_screen.show()
        self.close()

    def cerrar_sesion(self):
        from Vistas.LoginScreen import LoginScreen
        login_screen = LoginScreen()
        login_screen.show()
        self.close()

    def actualizarFiltros(self):
        if self.filtroNombre.isChecked():
            self.buscarNombre.setVisible(True)
        else:
            self.buscarNombre.setVisible(False)

        if self.filtroApellido.isChecked():
            self.buscarApellido.setVisible(True)
        else:
            self.buscarApellido.setVisible(False)

        if self.filtroCargo.isChecked():
            self.buscarCargo.setVisible(True)
        else:
            self.buscarCargo.setVisible(False)

        if self.filtroTurno.isChecked():
            self.buscarTurno.setVisible(True)
        else:
            self.buscarTurno.setVisible(False)

        if self.filtros.isChecked():
            self.filtroNombre.setVisible(True)
            self.filtroApellido.setVisible(True)
            self.filtroCargo.setVisible(True)
            self.filtroTurno.setVisible(True)
        else:
            self.filtroNombre.setVisible(False)
            self.filtroApellido.setVisible(False)
            self.filtroCargo.setVisible(False)
            self.filtroTurno.setVisible(False)

    def buscar_rendimiento_empleado(self):
        fechaInput = self.fechaRendimiento.text()
        id = self.idRendimiento.text()

        if fechaInput and id:
            with EmpleadosDatabase() as empleados_data:
                empleados_data.buscar_rendimiento_empleado(id, fechaInput, self.tablaDatos)

            self.errorIdFecha.setVisible(False)
        else:
            self.errorIdFecha.setVisible(True)

    def actualizarFiltroNombre(self, texto):
        if texto:
            with EmpleadosDatabase() as empleados_data:
                query = "SELECT * FROM empleados_parametros WHERE nombre LIKE ?"
                params = [f"%{texto}%"]
                empleados_data.filtrar_por_campos(
                    query, params, self.tablaDatos)

    def actualizarFiltroApellido(self, texto):
        if texto:
            with EmpleadosDatabase() as empleados_data:
                query = "SELECT * FROM empleados_parametros WHERE apellido LIKE ?"
                params = [f"%{texto}%"]
                empleados_data.filtrar_por_campos(
                    query, params, self.tablaDatos)

    def actualizarFiltroCargo(self, texto):
        if texto:
            with EmpleadosDatabase() as empleados_data:
                query = "SELECT * FROM empleados_parametros WHERE cargo LIKE ?"
                params = [f"%{texto}%"]
                empleados_data.filtrar_por_campos(
                    query, params, self.tablaDatos)

    def actualizarFiltroTurno(self, texto):
        if texto:
            with EmpleadosDatabase() as empleados_data:
                query = "SELECT * FROM empleados_parametros WHERE turno LIKE ?"
                params = [f"%{texto}%"]
                empleados_data.filtrar_por_campos(
                    query, params, self.tablaDatos)
