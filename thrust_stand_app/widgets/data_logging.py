from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QCheckBox, QHBoxLayout,
                            QGroupBox, QPushButton, QLabel, QFileDialog, 
                            QMessageBox, QFrame, QScrollArea, QSizePolicy)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon, QFont
from datetime import datetime
import csv
import shutil
import os

class DataLogging(QWidget):
    def __init__(self, data_simulator):
        super().__init__()
        self.data_simulator = data_simulator
        self.logging_active = False
        self.log_timer = QTimer()
        self.start_time = None
        self.log_file = None
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Left panel for parameter selection
        left_panel = QVBoxLayout()
        
        # Parameter Selection Group
        param_group = QGroupBox("Logging Parameters")
        param_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        param_scroll = QScrollArea()
        param_scroll.setWidgetResizable(True)
        param_scroll.setFrameShape(QFrame.NoFrame)
        
        param_container = QWidget()
        param_layout = QVBoxLayout(param_container)
        param_layout.setSpacing(10)
        
        # Select All option
        select_all = QCheckBox("Select All Parameters")
        select_all.setStyleSheet("font-weight: bold; font-size: 12px;")
        select_all.stateChanged.connect(self.toggle_select_all)
        param_layout.addWidget(select_all)
        
        # Add a separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        param_layout.addWidget(separator)
        
        # Motor Parameters
        motor_group = QGroupBox("Motor Parameters")
        motor_group.setStyleSheet("""
            QGroupBox {
                background-color: #e8f5e9;
                border: 1px solid #a5d6a7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #2e7d32;
            }
        """)
        
        motor_layout = QVBoxLayout()
        self.rpm_check = QCheckBox("RPM")
        self.temp_check = QCheckBox("Temperature")
        
        # Style checkboxes
        checkbox_style = """
            QCheckBox {
                spacing: 10px;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #bbbbbb;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4CAF50;
                border-radius: 3px;
                background-color: #4CAF50;
            }
        """
        
        self.rpm_check.setStyleSheet(checkbox_style)
        self.temp_check.setStyleSheet(checkbox_style)
        
        motor_layout.addWidget(self.rpm_check)
        motor_layout.addWidget(self.temp_check)
        motor_group.setLayout(motor_layout)
        
        # Electrical Parameters
        elec_group = QGroupBox("Electrical Parameters")
        elec_group.setStyleSheet("""
            QGroupBox {
                background-color: #e3f2fd;
                border: 1px solid #90caf9;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #1565c0;
            }
        """)
        
        elec_layout = QVBoxLayout()
        self.current_check = QCheckBox("Current")
        self.voltage_check = QCheckBox("Voltage")
        self.power_check = QCheckBox("Power")
        
        self.current_check.setStyleSheet(checkbox_style)
        self.voltage_check.setStyleSheet(checkbox_style)
        self.power_check.setStyleSheet(checkbox_style)
        
        elec_layout.addWidget(self.current_check)
        elec_layout.addWidget(self.voltage_check)
        elec_layout.addWidget(self.power_check)
        elec_group.setLayout(elec_layout)
        
        # Add parameter groups to layout
        param_layout.addWidget(motor_group)
        param_layout.addWidget(elec_group)
        param_layout.addStretch()
        
        param_scroll.setWidget(param_container)
        param_group_layout = QVBoxLayout()
        param_group_layout.addWidget(param_scroll)
        param_group.setLayout(param_group_layout)
        
        left_panel.addWidget(param_group)
        
        # Right panel for status and controls
        right_panel = QVBoxLayout()
        
        # Status Panel
        status_group = QGroupBox("Logging Status")
        status_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        status_layout = QVBoxLayout()
        
        # Status indicators
        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.StyledPanel)
        status_frame.setStyleSheet("background-color: #f5f5f5; border-radius: 5px; padding: 10px;")
        
        status_indicators = QVBoxLayout(status_frame)
        
        self.status_label = QLabel("Status: Idle")
        self.status_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        self.duration_label = QLabel("Duration: 0:00")
        self.duration_label.setStyleSheet("font-size: 12px;")
        self.duration_label.setAlignment(Qt.AlignCenter)
        
        self.size_label = QLabel("Log Size: 0 KB")
        self.size_label.setStyleSheet("font-size: 12px;")
        self.size_label.setAlignment(Qt.AlignCenter)
        
        status_indicators.addWidget(self.status_label)
        status_indicators.addWidget(self.duration_label)
        status_indicators.addWidget(self.size_label)
        
        status_layout.addWidget(status_frame)
        status_group.setLayout(status_layout)
        
        # Control Buttons Group
        control_group = QGroupBox("Controls")
        control_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        btn_layout = QVBoxLayout()
        
        self.start_btn = QPushButton("Start Logging")
        self.start_btn.setMinimumHeight(40)
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        
        self.export_btn = QPushButton("Export Log File")
        self.export_btn.setMinimumHeight(40)
        self.export_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.export_btn)
        control_group.setLayout(btn_layout)
        
        # Add groups to right panel
        right_panel.addWidget(status_group)
        right_panel.addWidget(control_group)
        right_panel.addStretch()
        
        # Add panels to main layout
        main_layout.addLayout(left_panel, 1)
        
        # Add a separator
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        main_layout.addLayout(right_panel, 1)
        
        self.setLayout(main_layout)
        
        # Set default checked state for parameters
        self.rpm_check.setChecked(True)
        self.current_check.setChecked(True)
        self.voltage_check.setChecked(True)

    def connect_signals(self):
        self.log_timer.timeout.connect(self.update_log_stats)
        self.start_btn.clicked.connect(self.toggle_logging)
        self.export_btn.clicked.connect(self.export_log_file)

    def toggle_logging(self):
        self.logging_active = not self.logging_active
        
        if self.logging_active:
            self.start_logging()
        else:
            self.stop_logging()
            
        self.update_ui_state()

    def start_logging(self):
        # Check if at least one parameter is selected
        if not any([self.rpm_check.isChecked(), self.temp_check.isChecked(),
                   self.current_check.isChecked(), self.voltage_check.isChecked(),
                   self.power_check.isChecked()]):
            QMessageBox.warning(self, "Logging Error", 
                               "Please select at least one parameter to log.")
            self.logging_active = False
            return
            
        filename = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.log_file = open(filename, 'w', newline='')
        self.writer = csv.writer(self.log_file)
        
        # Write header
        headers = ['timestamp'] + self.get_selected_params()
        self.writer.writerow(headers)
        
        self.start_time = datetime.now()
        self.log_timer.start(100)  # Update every 100ms
        
        self.update_ui_state()

    def stop_logging(self):
        if self.log_file:
            self.log_file.close()
            
        self.log_timer.stop()
        self.update_ui_state()

    def update_ui_state(self):
        if self.logging_active:
            self.status_label.setText("Status: Logging")
            self.status_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #4CAF50;")
            self.start_btn.setText("Stop Logging")
            self.start_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    font-weight: bold;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #e53935;
                }
                QPushButton:pressed {
                    background-color: #d32f2f;
                }
            """)
        else:
            self.status_label.setText("Status: Idle")
            self.status_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
            self.start_btn.setText("Start Logging")
            self.start_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #388e3c;
                }
            """)
            
    def toggle_select_all(self, state):
        checkboxes = [self.rpm_check, self.temp_check,
                    self.current_check, self.voltage_check, self.power_check]
        for cb in checkboxes:
            cb.setChecked(state == 2)

    def get_selected_params(self):
        params = []
        if self.rpm_check.isChecked(): params.append('rpm')
        if self.temp_check.isChecked(): params.append('temp')
        if self.current_check.isChecked(): params.append('current')
        if self.voltage_check.isChecked(): params.append('voltage')
        if self.power_check.isChecked(): params.append('power')
        return params

    def update_log_stats(self):
        if self.start_time:
            elapsed = datetime.now() - self.start_time
            self.duration_label.setText(f"Duration: {elapsed.seconds//60:02d}:{elapsed.seconds%60:02d}")
            
        if self.log_file:
            file_size = self.log_file.tell()
            self.size_label.setText(f"Log Size: {file_size/1024:.2f} KB")

    def log_data(self, data):
        if self.logging_active and self.log_file:
            timestamp = datetime.now().isoformat()
            selected = self.get_selected_params()
            row = [timestamp] + [data.get(param, 0) for param in selected]
            self.writer.writerow(row)

    def export_log_file(self):
        # If no logging has occurred yet
        if not hasattr(self, 'log_file') or self.log_file is None:
            QMessageBox.warning(self, "Export Error", "No log file available to export.")
            return
            
        # Get the current log filename
        current_filename = self.log_file.name