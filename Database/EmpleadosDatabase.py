import sqlite3


class EmpleadosDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('mineria_de_datos.db')
        self.cursor = self.conn.cursor()

    def agregar_usuario(self, nombre, contrasenia, privilegios):
        query = "INSERT INTO usuarios VALUES (?, ?, ?)"
        self.cursor.execute(query, (nombre, contrasenia, privilegios))
        self.conn.commit()

    def buscar_datos_empleado(self, id, nombre, apellido):
        query = "SELECT * FROM empleados WHERE id = ? AND nombre = ? AND apellido = ?"

        try:
            self.cursor.execute(query, (id, nombre, apellido))
            resultados = self.cursor.fetchall()
            return resultados
        except Exception as e:
            print("Empleado no encontrado:", e)

    def buscar_rendimiento_empleado(self, id, fecha):
        query = "SELECT * FROM empleados_parametros WHERE id = ? AND fecha = ?"

        try:
            self.cursor.execute(query, (id, fecha))
            resultados = self.cursor.fetchall()
            return resultados
        except Exception as e:
            print("Error al buscar los datos del empleado en la base de datos:", str(e))
            return []

    def agregar_empleado(self, nombre, apellido, cargo, turno):
        query = "INSERT INTO empleados (nombre, apellido, cargo, turno) VALUES (?, ?, ?, ?)"

        try:
            self.cursor.execute(query, (nombre, apellido, cargo, turno))
            self.conn.commit()
            print("Empleado agregado correctamente a la base de datos.")
        except Exception as e:
            print("Error al agregar el empleado a la base de datos:", str(e))

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
