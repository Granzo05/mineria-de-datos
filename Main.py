import sys
from PyQt5 import QtWidgets

from Vistas.LoginScreen import LoginScreen

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LoginScreen()
    window.show()
    sys.exit(app.exec_())
