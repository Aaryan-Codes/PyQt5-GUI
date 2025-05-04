from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QFormLayout,
                            QLineEdit, QPushButton, QLabel, QMessageBox, QSizePolicy,
                            QGroupBox, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import numpy as np

class ProfileControl(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler  # Callback to send profile data
        self.profile_params = {}
        self.active_profile = None
        self.init_ui()
        
    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Left panel for profile selection and controls
        left_panel = QVBoxLayout()
        
        # Profile Type Selection Group
        profile_group = QGroupBox("Profile Selection")
        profile_layout = QVBoxLayout()
        
        self.profile_type = QComboBox()
        self.profile_type.addItems([
            "Sine Wave",
            "Step Function",
            "Ramp Function",
            "Chirp Signal"
        ])
        self.profile_type.setStyleSheet("font-size: 14px; padding: 5px;")
        
        profile_layout.addWidget(self.profile_type)
        profile_group.setLayout(profile_layout)
        
        # Control Buttons Group
        control_group = QGroupBox("Controls")
        btn_layout = QVBoxLayout()
        
        self.apply_btn = QPushButton("Apply Profile")
        self.apply_btn.setMinimumHeight(40)
        self.apply_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        
        self.start_btn = QPushButton("Start")
        self.start_btn.setMinimumHeight(40)
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setMinimumHeight(40)
        self.stop_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        self.stop_btn.setEnabled(False)
        
        btn_layout.addWidget(self.apply_btn)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        control_group.setLayout(btn_layout)
        
        # Add groups to left panel
        left_panel.addWidget(profile_group)
        left_panel.addWidget(control_group)
        left_panel.addStretch()
        
        # Right panel for parameters
        right_panel = QVBoxLayout()
        
        # Parameters Group
        params_group = QGroupBox("Profile Parameters")
        params_layout = QVBoxLayout()
        
        # Create a scroll area for parameters
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        params_container = QWidget()
        self.param_form = QFormLayout(params_container)
        self.param_form.setVerticalSpacing(10)
        self.param_form.setContentsMargins(5, 5, 5, 5)
        
        scroll_area.setWidget(params_container)
        params_layout.addWidget(scroll_area)
        params_group.setLayout(params_layout)
        
        right_panel.addWidget(params_group)
        
        # Add panels to main layout
        main_layout.addLayout(left_panel, 1)
        
        # Add a separator
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        main_layout.addLayout(right_panel, 2)
        
        self.setLayout(main_layout)
        
        # Connect signals
        self.profile_type.currentTextChanged.connect(self.update_parameters)
        self.apply_btn.clicked.connect(self.store_parameters)
        self.start_btn.clicked.connect(self.start_profile)
        self.stop_btn.clicked.connect(self.stop_profile)
        
        # Initialize with default parameters
        self.update_parameters(self.profile_type.currentText())
        
        # Apply global stylesheet
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #aaaaaa;
                border-radius: 3px;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #aaaaaa;
                border-radius: 3px;
            }
            QLabel {
                font-weight: bold;
            }
        """)

    def update_parameters(self, profile_type):
        # Clear existing parameters
        while self.param_form.rowCount() > 0:
            self.param_form.removeRow(0)
            
        # Common parameters
        title_label = QLabel("Profile Parameters")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        self.param_form.addRow(title_label)
        
        # Add a separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.param_form.addRow(separator)
        
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Seconds")
        
        if profile_type == "Sine Wave":
            self.add_sine_parameters()
        elif profile_type == "Step Function":
            self.add_step_parameters()
        elif profile_type == "Ramp Function":
            self.add_ramp_parameters()
        elif profile_type == "Chirp Signal":
            self.add_chirp_parameters()
            
        # Add duration at the end
        self.param_form.addRow(QLabel("Duration:"), self.duration_input)

    def add_sine_parameters(self):
        self.amplitude_input = QLineEdit()
        self.frequency_input = QLineEdit()
        self.offset_input = QLineEdit()
        
        self.amplitude_input.setPlaceholderText("RPM")
        self.frequency_input.setPlaceholderText("Hz")
        self.offset_input.setPlaceholderText("RPM")
        
        self.param_form.addRow(QLabel("Amplitude (RPM):"), self.amplitude_input)
        self.param_form.addRow(QLabel("Frequency (Hz):"), self.frequency_input)
        self.param_form.addRow(QLabel("Offset (RPM):"), self.offset_input)

    def add_step_parameters(self):
        steps_container = QWidget()
        self.steps_layout = QVBoxLayout(steps_container)
        self.steps_layout.setContentsMargins(0, 0, 0, 0)
        self.step_widgets = []
        
        add_step_btn = QPushButton("+ Add Step")
        add_step_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        add_step_btn.clicked.connect(self.add_step_row)
        
        self.param_form.addRow(QLabel("Steps:"))
        self.param_form.addRow(steps_container)
        self.param_form.addRow(add_step_btn)
        
        self.add_step_row()  # Add initial step

    def add_ramp_parameters(self):
        self.start_rpm_input = QLineEdit()
        self.end_rpm_input = QLineEdit()
        self.ramp_time_input = QLineEdit()
        
        self.start_rpm_input.setPlaceholderText("RPM")
        self.end_rpm_input.setPlaceholderText("RPM")
        self.ramp_time_input.setPlaceholderText("Seconds")
        
        self.param_form.addRow(QLabel("Start RPM:"), self.start_rpm_input)
        self.param_form.addRow(QLabel("End RPM:"), self.end_rpm_input)
        self.param_form.addRow(QLabel("Ramp Time (s):"), self.ramp_time_input)

    def add_chirp_parameters(self):
        self.start_freq_input = QLineEdit()
        self.end_freq_input = QLineEdit()
        self.amplitude_input = QLineEdit()
        
        self.start_freq_input.setPlaceholderText("Hz")
        self.end_freq_input.setPlaceholderText("Hz")
        self.amplitude_input.setPlaceholderText("RPM")
        
        self.param_form.addRow(QLabel("Start Freq (Hz):"), self.start_freq_input)
        self.param_form.addRow(QLabel("End Freq (Hz):"), self.end_freq_input)
        self.param_form.addRow(QLabel("Amplitude (RPM):"), self.amplitude_input)

    def add_step_row(self):
        step_frame = QFrame()
        step_frame.setFrameShape(QFrame.StyledPanel)
        step_frame.setStyleSheet("background-color: #f5f5f5; border-radius: 5px;")
        
        row = QHBoxLayout(step_frame)
        rpm_input = QLineEdit()
        duration_input = QLineEdit()
        
        rpm_input.setPlaceholderText("RPM")
        duration_input.setPlaceholderText("Seconds")
        
        remove_btn = QPushButton("×")
        remove_btn.setStyleSheet("color: white; font-weight: bold; background-color: #f44336; border-radius: 15px;")
        remove_btn.setFixedSize(30, 30)
        
        row.addWidget(QLabel("RPM:"))
        row.addWidget(rpm_input)
        row.addWidget(QLabel("Duration (s):"))
        row.addWidget(duration_input)
        row.addWidget(remove_btn)
        
        self.steps_layout.addWidget(step_frame)
        self.step_widgets.append((rpm_input, duration_input, remove_btn, step_frame))
        
        remove_btn.clicked.connect(lambda: self.remove_step_row(step_frame))

    def remove_step_row(self, frame):
        frame.deleteLater()
        self.step_widgets = [w for w in self.step_widgets if w[3] != frame]

    def validate_inputs(self):
        try:
            profile_type = self.profile_type.currentText()
            duration = float(self.duration_input.text())
            
            if profile_type == "Sine Wave":
                return {
                    'type': 'sine',
                    'amplitude': float(self.amplitude_input.text()),
                    'frequency': float(self.frequency_input.text()),
                    'offset': float(self.offset_input.text()),
                    'duration': duration
                }
            elif profile_type == "Step Function":
                steps = []
                for rpm_input, duration_input, _, _ in self.step_widgets:
                    steps.append({
                        'rpm': float(rpm_input.text()),
                        'duration': float(duration_input.text())
                    })
                return {
                    'type': 'step',
                    'steps': steps,
                    'duration': duration
                }
            elif profile_type == "Ramp Function":
                return {
                    'type': 'ramp',
                    'start_rpm': float(self.start_rpm_input.text()),
                    'end_rpm': float(self.end_rpm_input.text()),
                    'ramp_time': float(self.ramp_time_input.text()),
                    'duration': duration
                }
            elif profile_type == "Chirp Signal":
                return {
                    'type': 'chirp',
                    'start_freq': float(self.start_freq_input.text()),
                    'end_freq': float(self.end_freq_input.text()),
                    'amplitude': float(self.amplitude_input.text()),
                    'duration': duration
                }
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", f"Invalid input value: {str(e)}")
            return None

    def store_parameters(self):
        params = self.validate_inputs()
        if params:
            self.profile_params = params
            QMessageBox.information(self, "Success", "Profile parameters stored!")

    def start_profile(self):
        if not self.profile_params:
            QMessageBox.warning(self, "Error", "No profile parameters stored!")
            return
            
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.apply_btn.setEnabled(False)
        
        self.worker = ProfileWorker(self.profile_params)
        self.worker.data_updated.connect(self.data_handler)
        self.worker.start()

    def stop_profile(self):
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker._is_running = False
            self.worker.quit()
            self.worker.wait()
            
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.apply_btn.setEnabled(True)


class ProfileWorker(QThread):
    data_updated = pyqtSignal(float)
    
    def __init__(self, params):
        super().__init__()
        self.params = params
        self._is_running = True
        
    def run(self):
        if self.params['type'] == 'sine':
            t = np.linspace(0, self.params['duration'], int(self.params['duration']*100))
            for time_point in t:
                if not self._is_running: 
                    break
                rpm = self.params['offset'] + self.params['amplitude'] * np.sin(2 * np.pi * self.params['frequency'] * time_point)
                self.data_updated.emit(rpm)
                self.msleep(10)
                
        elif self.params['type'] == 'step':
            for step in self.params['steps']:
                if not self._is_running:
                    break
                duration = step['duration']
                rpm = step['rpm']
                iterations = int(duration * 100)  # 10ms steps
                for _ in range(iterations):
                    if not self._is_running:
                        break
