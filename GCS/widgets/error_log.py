from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QDateTime

class ErrorLogWidget(QGroupBox):
    def __init__(self):
        super().__init__("Error Log")
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #252526;
                margin-top: 15px;
            }
            QLabel {
                font: bold 12px;
            }
        """)
        self.max_entries = 100
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #1E1E1E;
                color: #FFFFFF;
                font: 10pt Monospace;
                border: none;
            }
        """)
        
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        self.setStyleSheet("""
            QGroupBox {
                font: bold 14px;
                color: #1E90FF;
                border: 2px solid #1E90FF;
                border-radius: 5px;
                margin-top: 10px;
            }
        """)

    def add_entry(self, error_data):
        if not error_data or not error_data.get('code'):
            return
            
        timestamp = QDateTime.currentDateTime().toString("[hh:mm:ss]")
        text = f"{timestamp} {error_data['code']}: {error_data['desc']} ({error_data['source']})"
        
        item = QListWidgetItem(text)
        item.setForeground(self._get_error_color(error_data['source']))
        
        self.list_widget.insertItem(0, item)
        
        # Maintain max entries
        while self.list_widget.count() > self.max_entries:
            self.list_widget.takeItem(self.max_entries)

    def _get_error_color(self, source):
        colors = {
            'Motors': QColor(255, 100, 100),     # Red
            'Battery': QColor(255, 200, 100),    # Orange
            'Flight Controller': QColor(100, 200, 255),  # Blue
            'Sensors': QColor(200, 100, 255)     # Purple
        }
        return colors.get(source, QColor(255, 255, 255))