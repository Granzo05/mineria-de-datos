import sys
from PyQt5 import QtWidgets
from Vistas.Menu import Menu

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Menu()
    window.show()
    sys.exit(app.exec_())

