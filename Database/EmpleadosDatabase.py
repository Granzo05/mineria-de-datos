import sqlite3
import uuid

class EmpleadosDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('mineria_de_datos.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """
        Crea las tablas en la base de datos si no existen.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS empleados (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                apellido TEXT,
                cargo TEXT,
                turno TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS empleados_parametros (
                id INTEGER PRIMARY KEY,
                fecha TEXT,
                pasos INTEGER,
                horas INTEGER,
                asistencia TEXT,
                ventas INTEGER,
                nivel_estres INTEGER,
                empleado_id INTEGER,
                FOREIGN KEY(empleado_id) REFERENCES empleados(id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nombre_usuario TEXT,
                contraseña TEXT,
                privilegios TEXT
            )
        ''')

    def agregar_usuario(self, nombre, contrasenia, privilegios):
        """
        Agrega un usuario a la tabla de usuarios.

        Args:
            nombre (str): Nombre del usuario.
            contrasenia (str): Contraseña del usuario.
            privilegios (str): Privilegios del usuario.
        """
        query = "INSERT INTO usuarios VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (nombre, contrasenia, privilegios))

        self.conn.commit()

    def buscar_usuario(self, nombre, contrasenia):
        """
        Busca un usuario en la tabla de usuarios.

        Args:
            nombre (str): Nombre del usuario.
            contrasenia (str): Contraseña del usuario.

        Returns:
            list: Lista de resultados de la búsqueda.
        """
        query = "SELECT * FROM usuarios WHERE nombre = ? AND contraseña = ?"
        self.cursor.execute(query, (nombre, contrasenia))

        resultados = self.cursor.fetchall()

        if resultados:
            return resultados
        else:
            return None

    def buscar_empleado(self, nombre=None, apellido=None, cargo=None, turno=None):
        """
        Busca empleados en la tabla de empleados según los criterios especificados.

        Args:
            nombre (str): Nombre del empleado (opcional).
            apellido (str): Apellido del empleado (opcional).
            cargo (str): Cargo del empleado (opcional).
            turno (str): Turno del empleado (opcional).

        Returns:
            list: Lista de resultados de la búsqueda.
        """
        query = "SELECT * FROM empleados WHERE"
        conditions = []

        if nombre:
            conditions.append("nombre = ?")
        if apellido:
            conditions.append("apellido = ?")
        if cargo:
            conditions.append("cargo = ?")
        if turno:
            conditions.append("turno = ?")

        if conditions:
            query += " AND ".join(conditions)

        self.cursor.execute(query, (nombre, apellido, cargo, turno))

        resultados = self.cursor.fetchall()
        return resultados

    def agregar_empleado(self, nombre, apellido, cargo, turno):
        """
        Agrega un empleado a la tabla de empleados.

        Args:
            nombre (str): Nombre del empleado.
            apellido (str): Apellido del empleado.
            cargo (str): Cargo del empleado.
            turno (str): Turno del empleado.
        """
        id_empleado = str(uuid.uuid4())

        query = "INSERT INTO empleados VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, (id_empleado, nombre, apellido, cargo, turno))

        self.conn.commit()

    def close_connection(self):
        """
        Cierra la conexión a la base de datos.
        """
        self.cursor.close()
        self.conn.close()
