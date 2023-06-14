from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate
import pandas as pd
import matplotlib.pyplot as plt

from Database.EmpleadosDatabase import EmpleadosDatabase


class EmpleadosScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(EmpleadosScreen, self).__init__()
        uic.loadUi("Interfaz/search.ui", self)

        self.volver.clicked.connect(lambda: self.volver_screen())
        self.salir.clicked.connect(self.salir_screen)
        self.cerrarSesion.clicked.connect(self.cerrar_sesion)
        self.ultimos31.clicked.connect(lambda: self.mostrar_empleados_por_parametros_graficos(dias=31))
        self.ultimos14.clicked.connect(lambda: self.mostrar_empleados_por_parametros_graficos(dias=14))

        self.errorIdFecha.setVisible(False)
        self.buscarNombre.setVisible(False)
        self.buscarApellido.setVisible(False)
        self.buscarCargo.setVisible(False)
        self.buscarTurno.setVisible(False)
        self.diasGrafico.setVisible(False)
        self.turnoGrafico.setVisible(False)
        self.cargoGrafico.setVisible(False)
        self.idGrafico.setVisible(False)
        self.filtroNombre.setVisible(False)
        self.filtroApellido.setVisible(False)
        self.filtroCargo.setVisible(False)
        self.filtroTurno.setVisible(False)
        self.filtroTurnoGrafico.setVisible(False)
        self.filtroCargoGrafico.setVisible(False)
        self.filtroIdGrafico.setVisible(False)
        self.filtroDiasGrafico.setVisible(False)
        self.filtros.stateChanged.connect(self.actualizarFiltros)
        self.filtroPerso.stateChanged.connect(self.actualizarFiltrosGrafico)
        self.filtroPerso.setVisible(False)
        self.busquedaPersonalizada.setVisible(False)


        # Filtros para buscar empleados
        self.filtroNombre.stateChanged.connect(self.actualizarFiltros)
        self.filtroApellido.stateChanged.connect(self.actualizarFiltros)
        self.filtroCargo.stateChanged.connect(self.actualizarFiltros)
        self.filtroTurno.stateChanged.connect(self.actualizarFiltros)

        # Filtros para los graficos
        self.filtroTurnoGrafico.stateChanged.connect(self.actualizarFiltrosGrafico)
        self.filtroCargoGrafico.stateChanged.connect(self.actualizarFiltrosGrafico)
        self.filtroIdGrafico.stateChanged.connect(self.actualizarFiltrosGrafico)
        self.filtroDiasGrafico.stateChanged.connect(self.actualizarFiltrosGrafico)

        self.buscarRendimiento.clicked.connect(self.buscar_rendimiento_empleado)

        # Campos para buscar Empleados
        self.buscarNombre.textChanged.connect(self.actualizar_empleados_por_parametros)
        self.buscarApellido.textChanged.connect(self.actualizar_empleados_por_parametros)
        self.buscarCargo.textChanged.connect(self.actualizar_empleados_por_parametros)
        self.buscarTurno.textChanged.connect(self.actualizar_empleados_por_parametros)

        # Campos para crear grafico
        self.diasGrafico.textChanged.connect(self.actualizar_empleados_por_parametros_graficos)
        self.turnoGrafico.textChanged.connect(self.actualizar_empleados_por_parametros_graficos)
        self.cargoGrafico.textChanged.connect(self.actualizar_empleados_por_parametros_graficos)
        self.idGrafico.textChanged.connect(self.actualizar_empleados_por_parametros_graficos)

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
        try:
            from Vistas.LoginScreen import LoginScreen
            login_screen = LoginScreen()
            login_screen.show()
            self.close()
        except Exception as e:
            print(f"Error al abrir la ventana: {str(e)}")

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

    def actualizarFiltrosGrafico(self):
        if self.filtroTurnoGrafico.isChecked():
            self.turnoGrafico.setVisible(True)
        else:
            self.turnoGrafico.setVisible(False)

        if self.filtroCargoGrafico.isChecked():
            self.cargoGrafico.setVisible(True)
        else:
            self.cargoGrafico.setVisible(False)

        if self.filtroIdGrafico.isChecked():
            self.idGrafico.setVisible(True)
        else:
            self.idGrafico.setVisible(False)

        if self.filtroPerso.isChecked():
            self.filtroTurnoGrafico.setVisible(True)
            self.filtroCargoGrafico.setVisible(True)
            self.filtroIdGrafico.setVisible(True)
            self.diasGrafico.setVisible(True)
        else:
            self.filtroTurnoGrafico.setVisible(False)
            self.filtroCargoGrafico.setVisible(False)
            self.filtroIdGrafico.setVisible(False)
            self.filtroDiasGrafico.setVisible(False)

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

    def actualizar_empleados_por_parametros_graficos(self):
        dias = self.diasGrafico.text()
        turno = self.turnoGrafico.text()
        cargo = self.cargoGrafico.text()
        id = self.idGrafico.text()

        self.busquedaPersonalizada.clicked.connect(
            lambda: self.mostrar_empleados_por_parametros_graficos(dias, id, cargo, turno))
        self.errorIdFecha.setVisible(False)

    def mostrar_empleados_por_parametros_graficos(self, dias=None, id=None, cargo=None, turno=None):
        print(dias)
        print(turno)
        print(cargo)
        print(id)
        try:
            with EmpleadosDatabase() as empleados_data:
                query = "SELECT * FROM empleados WHERE 1=1"
                params = []

                if turno:
                    query += " AND turno LIKE ?"
                    params.append(f"%{turno}%")

                if cargo:
                    query += " AND cargo LIKE ?"
                    params.append(f"%{cargo}%")

                if id:
                    query += " AND id LIKE ?"
                    params.append(f"%{id}%")

                if id and cargo:
                    query += " AND (id LIKE ? AND cargo LIKE ?)"
                    params.extend([f"%{id}%", f"%{cargo}%"])

                if id and turno:
                    query += " AND (id LIKE ? AND turno LIKE ?)"
                    params.extend([f"%{id}%", f"%{turno}%"])

                if cargo and turno:
                    query += " AND (cargo LIKE ? AND turno LIKE ?)"
                    params.extend([f"%{cargo}%", f"%{turno}%"])

                # Obtener los IDs de los empleados que coinciden con los filtros
                ids_empleados = empleados_data.filtrar_por_campos_grafico(query, params)

        except Exception as e:
            print("Error al obtener los empleados:", str(e))

        with EmpleadosDatabase() as empleados_data:
            resultados = empleados_data.filtrar_por_campos_para_graficar(dias, ids_empleados)

        # Convertir la lista de empleados en un DataFrame de pandas
        df = pd.DataFrame(resultados,
                          columns=['fecha', 'pasos_realizados', 'horas_de_trabajo', 'asistencia', 'nivel_estres',
                                   'empleado_id'])

        df['fecha'] = pd.to_datetime(df['fecha'])

        filtro_dias = df[df['fecha'] >= pd.Timestamp.now() - pd.DateOffset(days=dias)]

        # Calcular las sumas de los parámetros para todos los empleados en un día
        suma_pasos = filtro_dias.groupby('fecha')['pasos_realizados'].sum()
        suma_horas_trabajo = filtro_dias.groupby('fecha')['horas_de_trabajo'].sum()
        suma_asistencia = filtro_dias.groupby('fecha')['asistencia'].apply(
            lambda x: (x == 'Presente').sum())
        suma_estres = filtro_dias.groupby('fecha')['nivel_estres'].mean()

        # Crear gráfico para los pasos
        plt.subplot(2, 1, 1)
        plt.plot(suma_pasos.index, suma_pasos, label='Pasos Realizados')
        plt.xlabel('Fecha')
        plt.ylabel('Pasos')
        plt.title('Pasos Realizados en los últimos {} días'.format(dias))
        plt.xticks(rotation=45)
        plt.legend()

        # Crear gráfico combinado para el estrés, asistencia y horas
        plt.subplot(2, 1, 2)
        plt.plot(suma_horas_trabajo.index, suma_horas_trabajo, label='Horas de Trabajo')
        plt.plot(suma_asistencia.index, suma_asistencia, label='Asistencia')
        plt.plot(suma_estres.index, suma_estres, label='Nivel de Estrés')
        plt.xlabel('Fecha')
        plt.ylabel('Valor')
        plt.title('Horas de Trabajo, Asistencia y Nivel de Estrés en los últimos {} días'.format(dias))
        plt.xticks(rotation=45)
        plt.legend()

        # Mostrar ambos gráficos
        plt.tight_layout()
        plt.show()
