from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QFrame
from PyQt5.QtCore import Qt,QSize

class BatteryWidget(QWidget):
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

        self.layout.addWidget(self._section_title("Battery Status"))

        self.battery_widgets = []

        for i in range(4):  # 4 batteries
            container = QFrame()
            container.setFrameShape(QFrame.StyledPanel)
            container.setStyleSheet("""background-color: #f9f9f9; border-radius: 8px; padding: 6px;""")
            hbox = QHBoxLayout(container)

            name_label = QLabel(f"Battery {i+1}")
            name_label.setFixedWidth(80)

            progress = QProgressBar()
            progress.setMaximum(100)
            progress.setFormat("%p%")
            progress.setFixedHeight(30)
            progress.setStyleSheet("""
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
            progress.setAlignment(Qt.AlignCenter)

            temp_label = QLabel("Temp: 0°C")
            temp_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            temp_label.setFixedWidth(100)

            hbox.addWidget(name_label)
            hbox.addWidget(progress)
            hbox.addWidget(temp_label)

            self.layout.addWidget(container)
            self.battery_widgets.append((progress, temp_label))

    def _section_title(self, text):
        label = QLabel(f"<b>{text}</b>")
        label.setStyleSheet("""font-size: 16px;
                            color: #D4D4D4;
                            """)
        return label

    def update_data(self, levels, temps):
        for i in range(4):
            charge = int(levels[i])
            temp = temps[i]

            progress, temp_label = self.battery_widgets[i]
            progress.setValue(charge)

            # Style progress chunk color based on charge
            if charge < 30:
                chunk_color = "#f44336"  # red
            elif charge < 60:
                chunk_color = "#ff9800"  # orange
            else:
                chunk_color = "#4caf50"  # green

            progress.setStyleSheet(f"""
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

            # Update temperature label
            temp_label.setText(f"Temp: {temp:.1f}°C")
            if temp > 65:
                temp_label.setStyleSheet("color: red;")
            elif temp > 50:
                temp_label.setStyleSheet("color: orange;")
            else:
                temp_label.setStyleSheet("color: green;")
