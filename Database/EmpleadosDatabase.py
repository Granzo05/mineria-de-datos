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
            query += " LIMIT 1"
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

    def agregar_empleado(self, nombre, apellido, cargo, turno):
        try:
            sql = "INSERT INTO empleados (nombre, apellido, cargo, turno) VALUES (?, ?, ?, ?)"

            # Valores a insertar
            valores = (nombre, apellido, cargo, turno)

            # Ejecutar la sentencia SQL
            self.conn.execute(sql, valores)

            # Guardar los cambios
            self.conn.commit()
            print("Listo")
        except Exception as e:
            print("Error al agregar empleado:", str(e))

    def filtrar_por_campos(self, query, params, tablaEmpleados):
        try:
            self.cursor.execute(query, params)
            resultados = self.cursor.fetchall()

            tablaEmpleados.clearContents()
            tablaEmpleados.setRowCount(0)

            columnas = ["ID", "NOMBRE", "APELLIDO", "CARGO", "TURNO"]
            tablaEmpleados.setColumnCount(len(columnas))
            tablaEmpleados.setHorizontalHeaderLabels(columnas)

            num_rows = len(resultados)
            tablaEmpleados.setRowCount(num_rows)

            ids_empleados = []
            for row, resultado in enumerate(resultados):
                id_empleado = resultado[0]
                ids_empleados.append(id_empleado)

                for col, valor in enumerate(resultado):
                    item = QTableWidgetItem(str(valor))
                    tablaEmpleados.setItem(row, col, item)

            tablaEmpleados.resizeColumnsToContents()

            return ids_empleados

        except Exception as e:
            print("Error al filtrar por nombre en la base de datos:", str(e))

    def obtener_parametros_empleados_filtrados(self, ids, tablaDatos):
        try:
            with EmpleadosDatabase() as empleados_data:
                # Establecer las columnas a mostrar en la tabla
                columnas = ["ID", "FECHA", "PASOS", "HORAS TRABAJADAS", "ASISTENCIA", "NIVEL DE ESTRES"]
                tablaDatos.setColumnCount(len(columnas))
                tablaDatos.setHorizontalHeaderLabels(columnas)

                # Limpiar la tabla antes de agregar nuevos datos
                tablaDatos.clearContents()
                tablaDatos.setRowCount(0)

                ids = ids[0].strip('%[]')
                # Dividir la cadena en una lista de cadenas separadas por comas
                ids_list = ids.split(',')
                # Convertir cada cadena a un número entero
                ids = [int(id_str.strip()) for id_str in ids_list]

                # Construir la parte de la consulta con los marcadores de posición
                placeholders = ",".join(["?"] * len(ids))

                # Construir la consulta SQL con los marcadores de posición
                query = f"""
                    SELECT empleado_id, fecha, pasos_realizados, horas_de_trabajo, asistencia, nivel_estres
                    FROM empleados_parametros
                    WHERE empleado_id IN ({placeholders})
                """
                params = ids

                try:
                    self.cursor.execute(query, params)
                    resultados = self.cursor.fetchall()

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

        except Exception as e:
            print("Error al obtener los empleados:", str(e))

    def obtener_parametros_empleados_filtrados_grafico(self, ids):
        try:
            ids = ids[0].strip('%[]')
            # Dividir la cadena en una lista de cadenas separadas por comas
            ids_list = ids.split(',')
            # Convertir cada cadena a un número entero
            ids = [int(id_str.strip()) for id_str in ids_list]

            # Construir la parte de la consulta con los marcadores de posición
            placeholders = ",".join(["?"] * len(ids))

            # Construir la consulta SQL con los marcadores de posición
            query = f"""
                    SELECT fecha, pasos_realizados, horas_de_trabajo, asistencia, nivel_estres, empleado_id
                    FROM empleados_parametros
                    WHERE empleado_id IN ({placeholders})
                """
            params = ids

            try:
                self.cursor.execute(query, params)
                resultados = self.cursor.fetchall()

                return resultados

            except Exception as e:
                print("Error al buscar los datos del empleado en la base de datos:", str(e))
                return []

        except Exception as e:
            print("Error al obtener los empleados:", str(e))

    def filtrar_por_campos_para_graficar(self, dias, ids):
        try:
            if ids:
                ids = str(ids[0]).strip('%[]')
                # Dividir la cadena en una lista de cadenas separadas por comas
                ids_list = ids.split(',')
                # Convertir cada cadena a un número entero
                ids = [int(id_str.strip()) for id_str in ids_list]
            else:
                ids = []

            # Construir la parte de la consulta con los marcadores de posición
            placeholders = ",".join(["?"] * len(ids))

            # Construir la consulta SQL con los marcadores de posición
            query = f"SELECT DISTINCT fecha, pasos_realizados, horas_de_trabajo, asistencia, nivel_estres, empleado_id FROM empleados_parametros WHERE fecha >= DATE('now', '-{dias} day') AND empleado_id IN ({placeholders}) AND pasos_realizados IS NOT NULL"
            params = ids
            try:
                self.cursor.execute(query, params)
                resultados_db = self.cursor.fetchall()
                return resultados_db

            except Exception as e:
                print("Error al buscar los datos del empleado en la base de datos:", str(e))
                return []

        except Exception as e:
            print("Error al obtener los empleados:", str(e))

    def filtrar_por_campos_grafico(self, query, params):
        try:
            self.cursor.execute(query, params)
            resultados = self.cursor.fetchall()

            ids_empleados = [resultado[0] for resultado in resultados]

            return ids_empleados

        except Exception as e:
            print("Error al filtrar por campos en la base de datos:", str(e))

    def filtrar_por_campos_empleado(self, id, tablaEmpleados):
        query = "SELECT * FROM empleados WHERE id = ?"
        try:
            self.cursor.execute(query, id)
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


