import sys

from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QAction


class window(QMainWindow):
    def __init__(self):

        super().__init__()

    def createUI(self):


        self.setGeometry(500, 300, 700, 700)

        self.setWindowTitle("window")


        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        menubar = self.menuBar()
        fmenu = menubar.addMenu("File")
        fmenu.addAction(quit)

    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("You sure?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

main = QApplication(sys.argv)
window = window()
window.createUI()
window.show()
sys.exit(main.exec_())