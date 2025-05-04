import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow
from utils.theme import DarkTheme

class GCSApplication:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyleSheet(DarkTheme.STYLESHEET)
        self.window = MainWindow()
        
        
    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())
        
