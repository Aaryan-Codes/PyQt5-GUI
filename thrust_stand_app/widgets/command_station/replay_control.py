from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QLabel, QFileDialog, QListWidget, QAbstractItemView,
                            QSlider, QGroupBox, QFrame, QSplitter, QFileIconProvider)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon, QFont
import csv
import os

class ReplayControl(QWidget):
    def __init__(self, data_handler):
        super().__init__()
        self.selected_file = None
        self.data_handler = data_handler
        self.replay_data = []
        self.replay_index = 0
        self.replay_timer = QTimer(self)  # Define timer before using it
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Left panel for file selection and saved runs
        left_panel = QVBoxLayout()
        
        # File Selection Group
        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout()
        
        file_btn_layout = QHBoxLayout()
        self.file_btn = QPushButton("Choose File")
        self.file_btn.setIcon(QIcon.fromTheme("document-open"))
        self.file_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 8px;")
        
        self.file_label = QLabel("No file chosen")
        self.file_label.setStyleSheet("font-style: italic; padding: 5px; background-color: #f5f5f5; border: 1px solid #ddd; border-radius: 3px;")
        
        file_btn_layout.addWidget(self.file_btn)
        file_layout.addLayout(file_btn_layout)
        file_layout.addWidget(self.file_label)
        
        file_group.setLayout(file_layout)
        
        # Saved Data List Group
        data_group = QGroupBox("Saved Runs")
        data_layout = QVBoxLayout()
        
        self.data_list = QListWidget()
        self.data_list.addItems(["Test Run 1", "Test Run 2", "Baseline Data"])
        self.data_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.data_list.setStyleSheet("""
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
        
        self.load_btn = QPushButton("Load Selected Run")
        self.load_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        
        data_layout.addWidget(self.data_list)
        data_layout.addWidget(self.load_btn)
        
        data_group.setLayout(data_layout)
        
        # Add groups to left panel
        left_panel.addWidget(file_group)
        left_panel.addWidget(data_group)
        left_panel.addStretch()
        
        # Right panel for playback controls
        right_panel = QVBoxLayout()
        
        # Playback Controls Group
        control_group = QGroupBox("Playback Controls")
        control_layout = QVBoxLayout()
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        self.play_button = QPushButton("Play")
        self.play_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.play_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; min-width: 80px; padding: 10px;")
        
        self.pause_button = QPushButton("Pause")
        self.pause_button.setIcon(QIcon.fromTheme("media-playback-pause"))
        self.pause_button.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; min-width: 80px; padding: 10px;")
        
        self.step_button = QPushButton("Step")
        self.step_button.setIcon(QIcon.fromTheme("media-skip-forward"))
        self.step_button.setStyleSheet("background-color: #9C27B0; color: white; font-weight: bold; min-width: 80px; padding: 10px;")
        
        buttons_layout.addWidget(self.play_button)
        buttons_layout.addWidget(self.pause_button)
        buttons_layout.addWidget(self.step_button)
        
        # Speed control layout
        speed_layout = QVBoxLayout()
        
        speed_label = QLabel("Playback Speed")
        speed_label.setAlignment(Qt.AlignCenter)
        speed_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50)
        self.speed_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: #ddd;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #2196F3;
                border: 1px solid #1565c0;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::sub-page:horizontal {
                background: #bbdefb;
                border-radius: 4px;
            }
        """)
        
        speed_value_layout = QHBoxLayout()
        speed_value_layout.addWidget(QLabel("Slow"))
        speed_value_layout.addStretch()
        speed_value_layout.addWidget(QLabel("Fast"))
        
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_slider)
        speed_layout.addLayout(speed_value_layout)
        
        # Playback status
        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.StyledPanel)
        status_frame.setStyleSheet("background-color: #f5f5f5; border-radius: 5px; padding: 10px;")
        
        status_layout = QVBoxLayout(status_frame)
        
        self.status_label = QLabel("Ready to play")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; color: #333;")
        
        self.progress_label = QLabel("0 / 0 frames")
        self.progress_label.setAlignment(Qt.AlignCenter)
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_label)
        
        # Assemble control layout
        control_layout.addLayout(buttons_layout)
        control_layout.addLayout(speed_layout)
        control_layout.addWidget(status_frame)
        
        control_group.setLayout(control_layout)
        
        # Add groups to right panel
        right_panel.addWidget(control_group)
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
        
        # Connect signals
        self.file_btn.clicked.connect(self.open_file_dialog)
        self.load_btn.clicked.connect(self.load_selected)
        self.replay_timer.timeout.connect(self.replay_next)
        self.play_button.clicked.connect(self.start_replay)
        self.pause_button.clicked.connect(self.pause_replay)
        self.step_button.clicked.connect(self.step_once)
        self.speed_slider.valueChanged.connect(self.change_speed)
        
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
        """)

    def load_selected(self):
        if not self.data_list.currentItem():
            self.status_label.setText("No run selected")
            return
            
        selected = self.data_list.currentItem().text()
        try:
            with open(f"{selected}.csv") as f:
                reader = csv.DictReader(f)
                self.replay_data = list(reader)
                self.replay_index = 0
                
            self.status_label.setText(f"Loaded: {selected}")
            self.progress_label.setText(f"0 / {len(self.replay_data)} frames")
            
        except Exception as e:
            self.status_label.setText(f"Error loading file: {str(e)}")

    def replay_next(self):
        if self.replay_index < len(self.replay_data):
            data = self.replay_data[self.replay_index]
            self.data_handler(data)
            self.replay_index += 1
            self.progress_label.setText(f"{self.replay_index} / {len(self.replay_data)} frames")
        else:
            self.replay_timer.stop()
            self.status_label.setText("Replay complete")

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open CSV", "", "CSV Files (*.csv)")
        if file_name:
            self.selected_file = file_name
            self.file_label.setText(os.path.basename(file_name))
            self.status_label.setText(f"File selected: {os.path.basename(file_name)}")
            
            # Load the file
            try:
                with open(file_name) as f:
                    reader = csv.DictReader(f)
                    self.replay_data = list(reader)
                    self.replay_index = 0
                    
                self.progress_label.setText(f"0 / {len(self.replay_data)} frames")
            except Exception as e:
                self.status_label.setText(f"Error loading file: {str(e)}")

    def start_replay(self):
        if not self.replay_data:
            self.status_label.setText("No data loaded")
            return
            
        self.replay_timer.start(100)
        self.status_label.setText("Playing...")

    def pause_replay(self):
        self.replay_timer.stop()
        self.status_label.setText("Paused")

    def step_once(self):
        self.replay_timer.stop()
        self.replay_next()
        self.status_label.setText("Stepped")

    def change_speed(self, value):
        # Convert slider value to interval (higher value = faster replay)
        interval = int(1000 / value)
        if self.replay_timer.isActive():
            self.replay_timer.stop()
            self.replay_timer.start(interval)
