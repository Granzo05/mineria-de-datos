from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate
import pandas as pd
import matplotlib.pyplot as plt

from Database.EmpleadosDatabase import EmpleadosDatabase


def crear_graficos(self):
    with EmpleadosDatabase() as empleados_data:
        empleados = empleados_data.obtener_parametros_empleados_graficos(30)

    # Convertir la lista de empleados en un DataFrame de pandas
    df = pd.DataFrame(empleados,
                      columns=['fecha', 'pasos_realizados', 'horas_de_trabajo', 'asistencia', 'nivel_estres',
                               'empleado_id'])

    # Eliminar las filas duplicadas basadas en la columna 'fecha'
    df = df.drop_duplicates(subset='fecha')

    df['fecha'] = pd.to_datetime(df['fecha'])

    # Crear gráficos individuales para cada parámetro
    # Crear gráficos individuales para cada parámetro
    parametros = ['pasos_realizados', 'horas_de_trabajo', 'asistencia_numerica', 'nivel_estres']

    for parametro in parametros:
        plt.figure()
        for empleado_id, empleado_data in df.groupby('empleado_id'):
            ultimos_30_dias = empleado_data[empleado_data['fecha'] >= pd.Timestamp.now() - pd.DateOffset(days=30)]
            ultimos_30_dias.loc[:, 'asistencia_numerica'] = ultimos_30_dias['asistencia'].apply(
                lambda x: 1 if x == 'Presente' else 0)
            plt.plot(ultimos_30_dias['fecha'], ultimos_30_dias[parametro], label=f'Empleado {empleado_id}')

        # Establecer etiquetas en el eje X
        plt.xticks(rotation=45)

        # Mostrar leyenda
        plt.legend()

    # Mostrar todos los gráficos juntos
    plt.show()


class EmpleadosScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(EmpleadosScreen, self).__init__()
        uic.loadUi("Interfaz/search.ui", self)

        self.volver.clicked.connect(lambda: self.volver_screen())
        self.salir.clicked.connect(self.salir_screen)
        self.cerrarSesion.clicked.connect(self.cerrar_sesion)
        # self.crarGraficos.clicked.connect(self.crear_graficos)

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

        self.buscarNombre.textChanged.connect(self.actualizar_empleados_por_parametros)
        self.buscarApellido.textChanged.connect(self.actualizar_empleados_por_parametros)
        self.buscarCargo.textChanged.connect(self.actualizar_empleados_por_parametros)
        self.buscarTurno.textChanged.connect(self.actualizar_empleados_por_parametros)

        fecha_inicio = QDate(2023, 4, 27)

        self.fechaRendimiento.setDate(fecha_inicio)

        crear_graficos(self)

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

    def actualizar_empleados_por_parametros(self):
        nombre = self.buscarNombre.text()
        apellido = self.buscarApellido.text()
        cargo = self.buscarCargo.text()
        turno = self.buscarTurno.text()

        self.mostrar_empleados_por_parametros(nombre, apellido, cargo, turno)

    def mostrar_empleados_por_parametros(self, nombre=None, apellido=None, cargo=None, turno=None):
        try:
            with EmpleadosDatabase() as empleados_data:
                query = "SELECT * FROM empleados WHERE 1=1"
                params = []

                if nombre:
                    query += " AND nombre LIKE ?"
                    params.append(f"%{nombre}%")

                if apellido:
                    query += " AND apellido LIKE ?"
                    params.append(f"%{apellido}%")

                if cargo:
                    query += " AND cargo LIKE ?"
                    params.append(f"%{cargo}%")

                if turno:
                    query += " AND turno LIKE ?"
                    params.append(f"%{turno}%")

                if nombre and apellido:
                    query += " AND (nombre LIKE ? AND apellido LIKE ?)"
                    params.extend([f"%{nombre}%", f"%{apellido}%"])

                if nombre and cargo:
                    query += " AND (nombre LIKE ? AND cargo LIKE ?)"
                    params.extend([f"%{nombre}%", f"%{cargo}%"])

                if cargo and turno:
                    query += " AND (cargo LIKE ? AND turno LIKE ?)"
                    params.extend([f"%{cargo}%", f"%{turno}%"])

                if nombre and turno:
                    query += " AND (nombre LIKE ? AND turno LIKE ?)"
                    params.extend([f"%{nombre}%", f"%{turno}%"])

                # Obtener los IDs de los empleados que coinciden con los filtros
                ids_empleados = empleados_data.filtrar_por_campos(query, params, self.tablaEmpleados)

                # Obtener los parámetros de los empleados filtrados
                params = [f"%{ids_empleados}%"]
                empleados_data.obtener_parametros_empleados_filtrados(params, self.tablaDatos)

        except Exception as e:
            print("Error al obtener los empleados:", str(e))
