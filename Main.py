import sys
from PyQt5 import QtWidgets

from Vistas.EmpleadosScreen import EmpleadosScreen
from Vistas.LoginScreen import LoginScreen

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = EmpleadosScreen()
    window.show()
    sys.exit(app.exec_())

