from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont

class AttitudeWidget(QGroupBox):
    def __init__(self):
        super().__init__("Attitude")
        self.setProperty("borderVisible", True)
        self.initUI()
        self.setStyleSheet("""
            QGroupBox {
                border: 2px solid #1E90FF;
                border-radius: 5px;
            }
            QLabel {
                font: bold 12px;
                color: #D4D4D4;
            }
        """)

    def initUI(self):
        layout = QVBoxLayout()
        
        self.roll_label = QLabel("Roll: 0.00°")
        self.pitch_label = QLabel("Pitch: 0.00°")
        self.yaw_label = QLabel("Yaw: 0.00°")
        self.setStyleSheet(
            """
            QGroupBox {
                border: 1px solid #252526;
                margin-top: 15px;
            }
            QLabel {
                font: bold 12px;
            }
        """
        )
        
        for label in [self.roll_label, self.pitch_label, self.yaw_label]:
            label.setFont(QFont('Monospace', 12))
            label.setStyleSheet("color: #FFFFFF;")
        
        layout.addWidget(self.roll_label)
        layout.addWidget(self.pitch_label)
        layout.addWidget(self.yaw_label)
        self.setLayout(layout)

    def update_attitude(self, roll, pitch, yaw=0.0):
        self.roll_label.setText(f"Roll: {roll:.2f}°")
        self.pitch_label.setText(f"Pitch: {pitch:.2f}°")
        self.yaw_label.setText(f"Yaw: {yaw:.2f}°")
        self.update()  # Important for visual refresh