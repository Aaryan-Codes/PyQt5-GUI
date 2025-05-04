from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QFrame
from PyQt5.QtCore import Qt

class MotorWidget(QWidget):
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
        
        self.layout.addWidget(self._section_title("Motor Status"))
        self.motor_widgets = []
        
        for i in range(7):
            container = QFrame()
            container.setFrameShape(QFrame.StyledPanel)
            container.setStyleSheet("""
                                    background-color: #f9f9f9;
                                    border-radius:8px;
                                    padding: 6px;
                                    """)
            hbox = QHBoxLayout(container)
            
            name_label = QLabel(f"Motor {i+1}")
            name_label.setFixedWidth(80)
            
            rpm_bar = QProgressBar()
            rpm_bar.setMaximum(10000)
            rpm_bar.setFormat("%p RPM")
            rpm_bar.setFixedHeight(30)
            rpm_bar.setStyleSheet("""
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
            
            temp_label = QLabel("Temp: 0°C")
            temp_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            temp_label.setFixedWidth(100)
            
            hbox.addWidget(name_label)
            hbox.addWidget(rpm_bar)
            hbox.addWidget(temp_label)
            
            self.layout.addWidget(container)
            self.motor_widgets.append((rpm_bar, temp_label))
            
    def _section_title(self,text):
        label = QLabel(f"<b>{text}</b>")
        label.setStyleSheet("font-size:16px; font-weight:bold;color: #D4D4D4;")
        return label
    
    def update_data(self,rpms,temps):
        for i in range(7):
            rpm = int(rpms[i])
            temp = temps[i]
            
            rpm_bar,temp_label = self.motor_widgets[i]
            rpm_bar.setValue(rpm)
            
            # RMP color feedback
            if rpm > 8000:
                chunk_color = "#e53935"  # red
            elif rpm > 6000:
                chunk_color = "#fb8c00"  # orange
            else:
                chunk_color = "#2196f3"  # blue
            rpm_bar.setStyleSheet(f"""
                                  QProgressBar{{
                                      border-radius: 8px;
                                      text-align: center;
                                      font-weight: bold;
                                  }}
                                  QProgressBar::chunk {{ 
                                  background-color: {chunk_color}; 
                                  border-radius: 8px;
                                  }}
                                  """)

            # Temperature label color
            temp_label.setText(f"Temp: {temp:.1f}°C")
            if temp > 85:
                temp_label.setStyleSheet("color: red;")
            elif temp > 70:
                temp_label.setStyleSheet("color: orange;")
            else:
                temp_label.setStyleSheet("color: green;") 