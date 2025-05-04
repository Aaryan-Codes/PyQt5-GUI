from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class SystemWidget(QGroupBox):
    def __init__(self):
        super().__init__("System Status")
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
        # self.setStyleSheet("""
        #     QGroupBox {
        #         font: bold 14px;
        #         color: #1E90FF;
        #         border: 2px solid #1E90FF;
        #         border-radius: 5px;
        #         margin-top: 10px;
        #         padding-top: 15px;
        #     }
        # """)
        
    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)
        
        # Initialize status indicators
        self.indicators = {
            'arm': StatusIndicator("DISARMED", QColor(255, 0, 0)),
            'mode': StatusIndicator("MANUAL", QColor(255, 165, 0)),
            'gps': StatusIndicator("NO FIX", QColor(255, 0, 0)),
            'link': StatusIndicator("LINK OK", QColor(0, 255, 0)),
            'imu': StatusIndicator("CALIBRATED", QColor(0, 255, 0)),
            'power': StatusIndicator("NOMINAL", QColor(0, 255, 0))
        }
        
        
        # Add to grid layout
        layout.addWidget(self._create_label("Armed:"), 0, 0)
        layout.addWidget(self.indicators['arm'], 0, 1)
        layout.addWidget(self._create_label("Flight Mode:"), 1, 0)
        layout.addWidget(self.indicators['mode'], 1, 1)
        layout.addWidget(self._create_label("GPS Status:"), 2, 0)
        layout.addWidget(self.indicators['gps'], 2, 1)
        layout.addWidget(self._create_label("Link:"), 3, 0)
        layout.addWidget(self.indicators['link'], 3, 1)
        layout.addWidget(self._create_label("IMU:"), 0, 2)
        layout.addWidget(self.indicators['imu'], 0, 3)
        layout.addWidget(self._create_label("Power:"), 1, 2)
        layout.addWidget(self.indicators['power'], 1, 3)

    def _create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font: bold 12px; color: #FFFFFF;")
        return label

    def update_status(self, armed, flight_mode, gps_sats, link_quality):
        # Update arm status
        self.indicators['arm'].set_state(
            armed,
            "ARMED" if armed else "DISARMED",
            QColor(0, 255, 0) if armed else QColor(255, 0, 0)
        )
        
        # Update flight mode
        mode_colors = {
            "MANUAL": QColor(255, 165, 0),
            "STABILIZE": QColor(0, 255, 255),
            "AUTO": QColor(0, 255, 0)
        }
        self.indicators['mode'].set_state(
            True,
            flight_mode,
            mode_colors.get(flight_mode, QColor(255, 165, 0))
        )
        
        # Update GPS status
        gps_state = gps_sats >= 6
        self.indicators['gps'].set_state(
            gps_state,
            f"FIX ({gps_sats}sats)" if gps_state else "NO FIX",
            QColor(0, 255, 0) if gps_state else QColor(255, 0, 0)
        )
        
        # Update link quality
        link_state = link_quality > 0.8
        self.indicators['link'].set_state(
            link_state,
            "LINK OK" if link_state else "WEAK LINK",
            QColor(0, 255, 0) if link_state else QColor(255, 165, 0)
        )

class StatusIndicator(QLabel):    
    def __init__(self, text, color):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumWidth(120)
        self.setMinimumHeight(25)
        self.setStyleSheet("""
            QLabel {
                border-radius: 4px;
                padding: 3px;
                font: bold 12px;
            }
        """)
        self.set_state(False, text, color)
        
    def set_state(self, active, text, color):
        self.setText(text)
        bg_color = color if active else QColor(60, 60, 60)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color.name()};
                color: {'black' if active else '#AAAAAA'};
                border-radius: 4px;
                padding: 3px;
                font: bold 12px;
            }}
        """)