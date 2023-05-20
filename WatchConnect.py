import sqlite3
import uuid
import datetime
import numpy as np
import schedule
import time


class EmpleadosData:
    def __init__(self):
        self.conn = sqlite3.connect('mineria_de_datos.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                apellido TEXT,
                cargo TEXT,
                turno TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios_parametros (
                id INTEGER PRIMARY KEY,
                fecha TEXT,
                pasos INTEGER,
                horas INTEGER,
                asistencia TEXT,
                ventas INTEGER,
                nivel_estres INTEGER,
                empleado_id INTEGER,
                FOREIGN KEY(empleado_id) REFERENCES usuarios(id)
            )
        ''')

    def buscar_usuario(self, nombre, apellido, cargo, turno):
        query = "SELECT * FROM usuarios WHERE nombre = ? AND apellido = ? AND cargo = ? AND turno = ?"
        self.cursor.execute(query, (nombre, apellido, cargo, turno))

        resultados = self.cursor.fetchall()

        for row in resultados:
            print(row)

    def agregar_usuario(self, nombre, apellido, cargo, turno):
        id_usuario = str(uuid.uuid4())

        query = "INSERT INTO usuarios VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, (id_usuario, nombre, apellido, cargo, turno))

        self.conn.commit()

    def obtener_datos_relojes(self):
        fecha_anterior = datetime.date.today() - datetime.timedelta(days=1)

        #client = Inicializar la biblioteca de sdk para acceder al reloj

        #client.autenticacion: Ver como autenticar cada usuario al que se acceda para ver de quien son los datos

        #activity_data = client.activity.get_activity_data() : obtiene todos los datos

        for activity in activity_data:
            fecha = str(fecha_anterior)
            pasos = activity.step_count
            horas = np.random.randint(6, 10)
            asistencia = np.random.choice(['Presente', 'Ausente'])
            ventas = np.random.randint(8, 25)
            nivel_estres = np.random.randint(0, 4)
            empleado_id = self.get_random_user_id()

            self.cursor.execute('''
                INSERT INTO usuarios_parametros (
                    id, fecha, pasos, horas, asistencia, ventas, nivel_estres, empleado_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (fecha, pasos, horas, asistencia, ventas, nivel_estres, empleado_id))

        self.conn.commit()

    def get_random_user_id(self):
        self.cursor.execute("SELECT id FROM usuarios")
        resultados = self.cursor.fetchall()
        ids = [row[0] for row in resultados]
        return np.random.choice(ids)

    def run_schedule(self):
        schedule.every().day.at("12:00").do(self.obtener_datos_relojes)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def close_connection(self):
        self.cursor.close()
        self.conn.close()


empleados_data = EmpleadosData()
empleados_data.run_schedule()