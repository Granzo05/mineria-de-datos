import datetime
import time

import numpy as np
import schedule

from EmpleadosDatabase import EmpleadosDatabase


class Scheduler:
    def __init__(self):
        self.empleados_data = EmpleadosDatabase()

    def obtener_datos_relojes(self):
        fecha_anterior = datetime.date.today() - datetime.timedelta(days=1)

        # client = Inicializar la biblioteca de sdk para acceder al reloj

        # client.autenticacion: Ver como autenticar cada empleado al que se acceda para ver de quien son los datos

        # activity_data = client.activity.get_activity_data() : obtiene todos los datos

        for activity in activity_data:
            fecha = str(fecha_anterior)
            pasos = activity.step_count
            horas = np.random.randint(6, 10)
            asistencia = np.random.choice(['Presente', 'Ausente'])
            ventas = np.random.randint(8, 25)
            nivel_estres = np.random.randint(0, 4)
            empleado_id = self.get_random_user_id()

            self.empleados_data.cursor.execute('''
                    INSERT INTO empleados_parametros (
                        id, fecha, pasos, horas, asistencia, ventas, nivel_estres, empleado_id
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (fecha, pasos, horas, asistencia, ventas, nivel_estres, empleado_id))

        self.empleados_data.conn.commit()

    def get_random_user_id(self):
        self.empleados_data.cursor.execute("SELECT id FROM empleados")
        resultados = self.empleados_data.cursor.fetchall()
        ids = [row[0] for row in resultados]
        return np.random.choice(ids)

    def run_schedule(self):
        schedule.every().day.at("12:00").do(self.obtener_datos_relojes)

        while True:
            schedule.run_pending()
            time.sleep(1)


scheduler = Scheduler()
scheduler.run_schedule()
