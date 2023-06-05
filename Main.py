import sys
from PyQt5 import QtWidgets
from Vistas.Menu import Menu

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    menu_screen = Menu()
    menu_screen.show()
    sys.exit(app.exec_())
