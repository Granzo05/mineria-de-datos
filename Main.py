from PyQt5 import QtWidgets

from Vistas.EmpleadosScreen import EmpleadosScreen
from Vistas.LoginScreen import LoginScreen
from Database.EmpleadosDatabase import EmpleadosDatabase


def main():
    app = QtWidgets.QApplication([])
    #window = LoginScreen()
    window = EmpleadosScreen()
    window.show()
    app.exec_()

    empleados_database = EmpleadosDatabase()
    empleados_database.close_connection()


if __name__ == "__main__":
    main()
