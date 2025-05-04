from PyQt5.QtWidgets import QGroupBox, QGridLayout, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt,QSize

class SensorWidget(QGroupBox):
    def __init__(self):
        super().__init__("Sensor Health")
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #252526;
                margin-top: 15px;
            }
            QLabel {
                font: bold 12px;
            }
        """)
        self.sensors = {
            'Accelerometer': 1,
            'Gyroscope': 1,
            'Magnetometer': 1,
            'Barometer': 1,
            'GPS': 1,
            'Pitot': 1
        }
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.indicators = {}
        
        for i, (name, status) in enumerate(self.sensors.items()):
            indicator = SensorIndicator(name)
            self.indicators[name] = indicator
            layout.addWidget(indicator, i//2, i%2)
            
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

    def update_status(self, sensor_health):
        for name, status in sensor_health.items():
            if name in self.indicators:
                self.indicators[name].set_state(status)

class SensorIndicator(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.state = 1  # 0=Bad, 1=Good, 2=Warning
        self.setMinimumSize(120, 40)

    def set_state(self, status):
        self.state = status
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # State colors
        colors = {
            0: QColor(255, 0, 0),    # Red
            1: QColor(0, 255, 0),    # Green
            2: QColor(255, 165, 0)   # Orange
        }
        
        # Draw indicator
        painter.setBrush(colors.get(self.state, QColor(255, 0, 0)))
        painter.drawEllipse(10, 10, 20, 20)
        
        # Draw text
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(40, 25, self.name)