import sqlite3


class EmpleadosDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('Database/mineria_de_datos.db')
        self.cursor = self.conn.cursor()

    def agregar_usuario(self, nombre, contrasenia, privilegios):
        query = "INSERT INTO usuarios VALUES (?, ?, ?)"
        self.cursor.execute(query, (nombre, contrasenia, privilegios))
        self.conn.commit()

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

    def buscar_datos_empleado(self, id, nombre, apellido, cargo, turno):
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
            print("Error al buscar los datos del empleado:", e)
            return []  # Devuelve una lista vacía en caso de excepción

    def buscar_rendimiento_empleado(self, id, fecha):
        query = "SELECT * FROM empleados_parametros WHERE empleado_id = ? AND fecha = ?"
        print(id, fecha)
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