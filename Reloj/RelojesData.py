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

        # Obtener los datos de pasos de Google Fit
        data = self.service.users().dataSources().datasets().get(
            userId='me',
            dataSourceId='derived:com.google.step_count.delta:com.google.android.gms:estimated_steps',
            datasetId='today',
        ).execute()
        pasos = data['point'][0]['value'][0]['intVal']

        horas = np.random.randint(6, 10)
        asistencia = np.random.choice(['Presente', 'Ausente'])
        ventas = np.random.randint(8, 25)
        nivel_estres = np.random.randint(0, 4)
        empleado_id = self.get_random_user_id()

        fecha = str(fecha_anterior)

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
