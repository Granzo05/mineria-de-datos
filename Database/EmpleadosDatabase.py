import sqlite3

from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidgetItem


class EmpleadosDatabase:
    def __init__(self):
        self.db_path = 'Database/mineria_de_datos.db'

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    def buscar_usuario(self, nombre, contrasenia):
        query = "SELECT * FROM usuarios WHERE nombre_usuario = ? AND contraseña = ?"

        try:
            self.cursor.execute(query, (nombre, contrasenia))
            resultado = self.cursor.fetchone()

            if resultado is not None:
                return True
            else:
                return False
        except Exception as e:
            print("Error al ejecutar la consulta:", e)

    def traer_empleados(self, tablaEmpleados):
        query = "SELECT * FROM empleados"
        try:
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            # Limpiar la tabla antes de agregar nuevos datos
            tablaEmpleados.clearContents()
            tablaEmpleados.setRowCount(0)

            # Establecer las columnas a mostrar en la tabla
            columnas = ["ID", "NOMBRE", "APELLIDO", "CARGO", "TURNO"]
            tablaEmpleados.setColumnCount(len(columnas))
            tablaEmpleados.setHorizontalHeaderLabels(columnas)

            # Calcular la cantidad de filas necesarias para mostrar los resultados
            num_rows = len(resultados)

            # Establecer la cantidad de filas en la tabla
            tablaEmpleados.setRowCount(num_rows)

            for row, resultado in enumerate(resultados):
                for col, valor in enumerate(resultado):
                    item = QTableWidgetItem(str(valor))
                    tablaEmpleados.setItem(row, col, item)

            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            tablaEmpleados.resizeColumnsToContents()
        except Exception as e:
            print("Error al obtener los empleados:", str(e))

    def obtener_parametros_empleados(self, tablaDatos):
        try:
            query = "SELECT fecha, pasos_realizados, horas_de_trabajo, asistencia, nivel_estres, empleado_id FROM empleados_parametros"
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()

            # Limpiar la tabla antes de agregar nuevos datos
            tablaDatos.clearContents()
            tablaDatos.setRowCount(0)

            # Establecer las columnas a mostrar en la tabla
            columnas = ["FECHA", "PASOS", "HORAS TRABAJADAS", "ASISTENCIA", "NIVEL DE ESTRES", "ID EMPLEADO"]
            tablaDatos.setColumnCount(len(columnas))
            tablaDatos.setHorizontalHeaderLabels(columnas)

            # Calcular la cantidad de filas necesarias para mostrar los resultados
            num_rows = len(resultados)

            # Establecer la cantidad de filas en la tabla
            tablaDatos.setRowCount(num_rows)

            for row, resultado in enumerate(resultados):
                for col, valor in enumerate(resultado):
                    item = QTableWidgetItem(str(valor))
                    tablaDatos.setItem(row, col, item)

            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            tablaDatos.resizeColumnsToContents()

        except Exception as e:
            print("Error al obtener los empleados:", str(e))

    def buscar_rendimiento_empleado(self, idEmpleado, fecha_input, tablaDatos):
        query = "SELECT * FROM empleados_parametros WHERE empleado_id = ?"
        params = []

        if fecha_input is not None:
            fecha_qdate = QtCore.QDate.fromString(fecha_input, "dd/MM/yyyy")
            if fecha_qdate.isValid() and fecha_qdate.dayOfWeek() < 6:
                fecha_final = fecha_qdate.toString(QtCore.Qt.DateFormat.ISODate)
                query += " AND fecha = ?"
            else:
                return []

        params.append(idEmpleado)
        params.append(fecha_final)

        try:
            self.cursor.execute(query, params)
            resultados = self.cursor.fetchall()

            # Limpiar la tabla antes de agregar nuevos datos
            tablaDatos.clearContents()
            tablaDatos.setRowCount(0)

            # Establecer las columnas a mostrar en la tabla
            columnas = ["ID", "FECHA", "PASOS", "HORAS TRABAJADAS", "ASISTENCIA", "NIVEL DE ESTRES", "ID EMPLEADO"]
            tablaDatos.setColumnCount(len(columnas))
            tablaDatos.setHorizontalHeaderLabels(columnas)

            # Calcular la cantidad de filas necesarias para mostrar los resultados
            num_rows = len(resultados)

            # Establecer la cantidad de filas en la tabla
            tablaDatos.setRowCount(num_rows)

            for row, resultado in enumerate(resultados):
                for col, valor in enumerate(resultado):
                    item = QTableWidgetItem(str(valor))
                    tablaDatos.setItem(row, col, item)

            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            tablaDatos.resizeColumnsToContents()
        except Exception as e:
            print("Error al buscar los datos del empleado en la base de datos:", str(e))
            return []

    def agregar_empleado(self, nombre, apellido, cargo, turno, errorEmpleado):
        query = "INSERT INTO empleados (nombre, apellido, cargo, turno) VALUES (?, ?, ?, ?)"
        try:
            self.cursor.execute(query, (nombre, apellido, cargo, turno))
            self.conn.commit()
        except Exception as e:
            errorEmpleado.setText("Error al agregar el empleado")
            errorEmpleado.show()
            # Configurar el temporizador para ocultar el label después de 2 segundos
            timer = QtCore.QTimer()
            timer.singleShot(2000, errorEmpleado.hide)
            print("Error al agregar el empleado:", str(e))

    def filtrar_por_campos(self, query, params, tablaDatos):
        try:
            self.cursor.execute(query, params)
            resultados = self.cursor.fetchall()

            tablaDatos.clearContents()
            tablaDatos.setRowCount(0)

            for row, resultado in enumerate(resultados):
                # Agregar cada valor del resultado a la tabla
                for col, valor in enumerate(resultado):
                    item = QTableWidgetItem(str(valor))
                    tablaDatos.setItem(row, col, item)

            tablaDatos.resizeColumnsToContents()
        except Exception as e:
            print("Error al filtrar por nombre en la base de datos:", str(e))

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
