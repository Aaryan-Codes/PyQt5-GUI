from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt,QSize

class GPSWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #252526;
                margin-top: 15px;
            }
            QLabel {
                font: bold 12px;
            }
        """)

        self.layout.addWidget(self._section_title("GPS Status"))

        self.hdop_bar = self._create_labeled_bar("HDOP", max_value=5.0)
        self.pdop_bar = self._create_labeled_bar("PDOP", max_value=5.0)

        self.sat_label = QLabel("Satellites: 0")
        self.sat_label.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.sat_label)

    def _section_title(self, text):
        label = QLabel(f"<b>{text}</b>")
        label.setStyleSheet("font-size: 16px;color: #D4D4D4;")
        return label

    def _create_labeled_bar(self, label_text, max_value):
        container = QFrame()
        container.setFrameShape(QFrame.StyledPanel)
        container.setStyleSheet("background-color: #f9f9f9; border-radius: 8px; padding: 6px;")

        layout = QHBoxLayout(container)

        label = QLabel(label_text)
        label.setFixedWidth(50)

        bar = QProgressBar()
        bar.setMaximum(int(max_value * 100))
        bar.setFormat("%.2f" % 0.0)
        bar.setFixedHeight(30)
        bar.setStyleSheet("""
            QProgressBar{ 
                border-radius: 8px; 
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #4caf50;
                border-radius: 8px;
            }
        """)
        bar.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)
        layout.addWidget(bar)
        self.layout.addWidget(container)
        return bar

    def update_data(self, gps_data):
        hdop = gps_data.get("HDOP", 0)
        pdop = gps_data.get("PDOP", 0)
        satellites = gps_data.get("satellites", 0)

        self.hdop_bar.setValue(int(hdop * 100))
        self.hdop_bar.setFormat(f"HDOP: {hdop:.2f}")

        self.pdop_bar.setValue(int(pdop * 100))
        self.pdop_bar.setFormat(f"PDOP: {pdop:.2f}")

        self.sat_label.setText(f"Satellites: {satellites}")
        self.sat_label.setStyleSheet("color: #D4D4D4;")

        # Color warnings (lower HDOP/PDOP = better)
        for bar, val in [(self.hdop_bar, hdop), (self.pdop_bar, pdop)]:
            chunk_color = "#4caf50"  # green (good)
            if val > 2.0:
                chunk_color = "#f44336"  # red (bad)
            elif val > 1.2:
                chunk_color = "#ff9800"  # orange (warning)
            
            bar.setStyleSheet(f"""
                QProgressBar {{
                    border-radius: 8px;
                    text-align: center;
                    font-weight: bold;
                }}
                QProgressBar::chunk {{
                    background-color: {chunk_color};
                    border-radius: 8px;
                }}
            """)
