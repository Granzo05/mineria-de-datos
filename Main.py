from PyQt5 import QtWidgets

from Database.LoginScreen import LoginScreen
from Database.EmpleadosDatabase import EmpleadosDatabase


def main():
    app = QtWidgets.QApplication([])
    window = LoginScreen()
    window.show()
    app.exec_()

    empleados_database = EmpleadosDatabase()
    empleados_database.close_connection()


if __name__ == "__main__":
    main()
