from PyQt5.QtWidgets import QWidget, QListWidgetItem, QVBoxLayout, QSlider, QLineEdit, QProgressBar, QPushButton, QListWidget, QLabel, QHBoxLayout, QGroupBox, QFrame
from PyQt5.QtCore import Qt
import json

class ManualControl(QWidget):
    def __init__(self, data_simulator):
        super().__init__()
        self.data_simulator = data_simulator
        self.init_ui()
        self.connect_signals()
        self.load_presets()
        
    def style_progress_bar(self, value=0):
        # Determine color based on RPM value
        if value < 3000:
            chunk_color = "#4caf50"  # green
        elif value < 7000:
            chunk_color = "#ff9800"  # orange
        else:
            chunk_color = "#f44336"  # red
            
        self.rpm_progress.setStyleSheet(f"""
            QProgressBar {{
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                height: 30px;
                font-size: 14px;
            }}
            QProgressBar::chunk {{
                background-color: {chunk_color};
                border-radius: 8px;
            }}
        """)
        
    def apply_preset(self, item):
        rpm = int(item.text().split('(')[1].split('RPM')[0].strip())
        self.rpm_slider.setValue(rpm)
        
    def save_preset(self):
        current_rpm = self.rpm_slider.value()
        preset_name = f"Custom ({current_rpm} RPM)"
        
        # Check if already exists
        for i in range(self.preset_list.count()):
            if self.preset_list.item(i).text() == preset_name:
                return
                
        self.preset_list.addItem(preset_name)
        
        # Save to file
        presets = []
        for i in range(self.preset_list.count()):
            presets.append(self.preset_list.item(i).text())
            
        with open('presets.json', 'w') as f:
            json.dump(presets, f)

    def load_presets(self):
        try:
            with open('presets.json') as f:
                presets = json.load(f)
                self.preset_list.clear()
                self.preset_list.addItems(presets)
        except FileNotFoundError:
            # Add default presets if file not found
            self.preset_list.clear()
            self.preset_list.addItems(["Idle (1000 RPM)", "Half Throttle (5000 RPM)", "Max Throttle (10000 RPM)"])

    def init_ui(self):
        main_layout = QHBoxLayout()
        
        # Left panel for options
        left_panel = QVBoxLayout()
        
        # Presets Group
        preset_group = QGroupBox("Presets")
        preset_layout = QVBoxLayout()
        
        self.preset_list = QListWidget()
        self.preset_list.setFixedHeight(150)
        self.preset_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                background-color: #f9f9f9;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1565c0;
            }
        """)
        
        preset_layout.addWidget(self.preset_list)
        preset_group.setLayout(preset_layout)
        
        # Control Buttons Group
        control_group = QGroupBox("Controls")
        btn_layout = QVBoxLayout()
        
        self.start_btn = QPushButton("Start")
        self.start_btn.setMinimumHeight(40)
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setMinimumHeight(40)
        self.reset_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        
        self.save_btn = QPushButton("Save Preset")
        self.save_btn.setMinimumHeight(40)
        self.save_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addWidget(self.save_btn)
        control_group.setLayout(btn_layout)
        
        # Add groups to left panel
        left_panel.addWidget(preset_group)
        left_panel.addWidget(control_group)
        left_panel.addStretch()
        
        # Right panel for RPM control
        right_panel = QVBoxLayout()
        
        rpm_group = QGroupBox("Manual RPM Control")
        rpm_layout = QVBoxLayout()
        
        # RPM Control
        self.rpm_slider = QSlider(Qt.Horizontal)
        self.rpm_slider.setRange(0, 10000)
        self.rpm_slider.setMinimumWidth(300)
        
        # RPM Input with label
        rpm_input_layout = QHBoxLayout()
        rpm_input_layout.addWidget(QLabel("RPM:"))
        self.rpm_input = QLineEdit()
        self.rpm_input.setStyleSheet("font-size: 14px; padding: 5px;")
        rpm_input_layout.addWidget(self.rpm_input)
        
        # RPM Progress Bar in a styled container
        progress_container = QFrame()
        progress_container.setFrameShape(QFrame.StyledPanel)
        progress_container.setStyleSheet("background-color: #f9f9f9; border-radius: 8px; padding: 6px;")
        
        progress_layout = QHBoxLayout(progress_container)
        
        rpm_label = QLabel("RPM")
        rpm_label.setFixedWidth(60)
        rpm_label.setStyleSheet("font-weight: bold;")
        
        self.rpm_progress = QProgressBar()
        self.rpm_progress.setMaximum(10000)
        self.rpm_progress.setFormat("%v RPM")
        self.rpm_progress.setFixedHeight(30)
        self.rpm_progress.setAlignment(Qt.AlignCenter)
        
        # Initial styling
        self.style_progress_bar()
        
        progress_layout.addWidget(rpm_label)
        progress_layout.addWidget(self.rpm_progress)
        
        rpm_layout.addWidget(self.rpm_slider)
        rpm_layout.addLayout(rpm_input_layout)
        rpm_layout.addWidget(progress_container)
        
        rpm_group.setLayout(rpm_layout)
        right_panel.addWidget(rpm_group)
        right_panel.addStretch()
        
        # Add panels to main layout
        main_layout.addLayout(left_panel, 1)
        
        # Add a separator
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        main_layout.addLayout(right_panel, 2)
        
        self.setLayout(main_layout)
        self.connect_signals()

    def connect_signals(self):
        self.rpm_slider.valueChanged.connect(self.update_rpm)
        self.preset_list.itemClicked.connect(self.apply_preset)
        self.save_btn.clicked.connect(self.save_preset)
        self.reset_btn.clicked.connect(lambda: self.rpm_slider.setValue(0))
        self.start_btn.clicked.connect(lambda: self.data_simulator.set_rpm(self.rpm_slider.value()))

    def update_rpm(self, value):
        self.data_simulator.set_rpm(value)
        self.rpm_input.setText(str(value))
        self.rpm_progress.setValue(value)
        
        # Update progress bar style based on the current value
        self.style_progress_bar(value)
