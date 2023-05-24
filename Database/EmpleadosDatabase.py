import sqlite3

from PyQt5 import QtCore
from PyQt5.QtCore import QDate

from Vistas.ResultadosBusqueda import ResultadosBusqueda


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

    def buscar_datos_empleado(self, id, nombre, apellido, cargo, turno, errorEmpleado):
        query = "SELECT * FROM empleados WHERE id = ?"
        parameters = [id]

        if nombre:
            query += " AND nombre = ?"
            parameters.append(nombre)

        if apellido:
            query += " AND apellido = ?"
            parameters.append(apellido)

        if cargo:
            query += " AND cargo = ?"
            parameters.append(cargo)

        if turno:
            query += " AND turno = ?"
            parameters.append(turno)

        try:
            self.cursor.execute(query, parameters)
            resultados = self.cursor.fetchall()
            return resultados
        except Exception as e:
            errorEmpleado.setText("Error al buscar los datos del empleado")
            errorEmpleado.show()
            # Configurar el temporizador para ocultar el label después de 2 segundos
            timer = QtCore.QTimer()
            timer.singleShot(2000, errorEmpleado.hide)
            print("Error al buscar los datos del empleado:", str(e))
            return []

    def buscar_rendimiento_empleado(self, id, fecha, errorEmpleado):
        fecha_qdate = QDate.fromString(fecha, "dd/MM/yyyy")

        if fecha_qdate.isValid() and fecha_qdate.dayOfWeek() < 6:
            fecha_formateada = fecha_qdate.toString("yyyy-MM-dd")
            fecha_formateada = fecha_formateada.replace("/", "-")
            try:
                query = "SELECT * FROM empleados_parametros WHERE empleado_id = ? AND fecha = ?"
                self.cursor.execute(query, (id, fecha))
                resultados = self.cursor.fetchall()
                resultados_window = ResultadosBusqueda(resultados)
                resultados_window.exec_()
            except Exception as e:
                print("Error al buscar los datos del empleado en la base de datos:", str(e))
                return []
        else:
            errorEmpleado.setText(fecha + " no fue un día laboral")
            errorEmpleado.show()
            # Configurar el temporizador para ocultar el label después de 2 segundos
            timer = QtCore.QTimer()
            timer.singleShot(2000, errorEmpleado.hide)

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

    def close_connection(self):
        self.cursor.close()
        self.conn.close()