from PyQt5 import QtWidgets

from Database.LoginScreen import LoginWindow
from Database.RelojesData import empleados_data


def main():
    app = QtWidgets.QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()

    empleados_data.close_connection()

if __name__ == "__main__":
    main()
