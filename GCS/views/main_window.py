from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QStackedLayout, QDockWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from views.ground_view import GroundView
from views.flight_view import FlightView
from utils.data_simulator import DataSimulator
from utils.logger import DataLogger
from widgets.error_log import ErrorLogWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ground Control Station")
        self.setGeometry(100, 100, 1400, 900)
        self.current_mode = "GROUND"
        
        
        # Initialize core components
        self.data_simulator = DataSimulator()
        self.logger = DataLogger()
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        # Central widget setup
        
        self.mode_label = QLabel("Ground Control Station")
        self.mode_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold;
            color: #FFFFFF;
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        
        # Create UI components
        self.create_top_bar()
        self.create_view_stack()
        self.create_dock_widgets()

    def create_top_bar(self):
        """Create the top control bar with a modern, uniform appearance"""
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)
        top_bar.setContentsMargins(10, 5, 10, 5)
        
        # Left section - GCS title and mode
        title_section = QVBoxLayout()
        
        self.mode_label = QLabel("Ground Control Station")
        self.mode_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold;
            color: #FFFFFF;
        """)
        
        self.status_label = QLabel("SYSTEM: INITIALIZING")
        self.status_label.setStyleSheet("""
            color: #FFA500;
            font: bold 14px;
            margin-top: 2px;
        """)
        
        title_section.addWidget(self.mode_label)
        title_section.addWidget(self.status_label)
        top_bar.addLayout(title_section)
        
        # Center spacer
        top_bar.addStretch(1)
        
        # Right section - Control buttons with consistent styling
        button_style = """
            QPushButton {
                min-width: 130px;
                min-height: 40px;
                padding: 8px;
                border-radius: 5px;
                font: bold 12px;
                margin: 0px 5px;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
        """
        
        # Control buttons with descriptive tooltips
        self.btn_arm = QPushButton("ARM DRONE")
        self.btn_arm.setToolTip("Arm or disarm the drone's motors")
        self.btn_arm.setStyleSheet(button_style + "background-color: #4CAF50; color: white;")
        
        self.btn_mode = QPushButton("MODE: MANUAL")
        self.btn_mode.setToolTip("Switch between manual and autonomous flight modes")
        self.btn_mode.setStyleSheet(button_style + "background-color: #2196F3; color: white;")
        
        self.btn_logging = QPushButton("START LOGGING")
        self.btn_logging.setToolTip("Begin or end data logging for this session")
        self.btn_logging.setStyleSheet(button_style + "background-color: #9C27B0; color: white;")
        
        self.btn_emergency = QPushButton("EMERGENCY STOP")
        self.btn_emergency.setToolTip("Immediately halt all drone operations")
        self.btn_emergency.setStyleSheet(button_style + "background-color: #F44336; color: white;")
        
        self.view_toggle_btn = QPushButton("SWITCH TO FLIGHT VIEW")
        self.view_toggle_btn.setToolTip("Toggle between ground station and flight views")
        self.view_toggle_btn.setStyleSheet(button_style + "background-color: #007ACC; color: white;")
        self.view_toggle_btn.clicked.connect(self.toggle_view)
        
        # Add buttons to top bar
        control_section = QHBoxLayout()
        control_section.setSpacing(8)
        control_section.addWidget(self.btn_arm)
        control_section.addWidget(self.btn_mode)
        control_section.addWidget(self.btn_logging)
        control_section.addWidget(self.btn_emergency)
        control_section.addWidget(self.view_toggle_btn)
        
        top_bar.addLayout(control_section)
        
        # Add the completed top bar to main layout
        self.main_layout.addLayout(top_bar)
        
        # Add a separator line
        separator = QWidget()
        separator.setFixedHeight(2)
        # Fix: Use Qt.SizePolicy instead of QWidget.Policy
        from PyQt5.QtWidgets import QSizePolicy
        separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        separator.setStyleSheet("background-color: #555555;")
        self.main_layout.addWidget(separator)

    def create_view_stack(self):
        """Create the view switcher"""
        self.view_stack = QStackedLayout()
        self.ground_view = GroundView()
        self.flight_view = FlightView()
        
        self.view_stack.addWidget(self.ground_view)
        self.view_stack.addWidget(self.flight_view)
        
        self.main_layout.addLayout(self.view_stack)
        
    def toggle_view(self):
        if self.current_mode == "GROUND":
            self.current_mode = "FLIGHT"
            self.view_toggle_btn.setText("Ground View")
            self.view_stack.setCurrentWidget(self.flight_view)
        else:
            self.current_mode = "GROUND"
            self.view_toggle_btn.setText("Flight View")
            self.view_stack.setCurrentWidget(self.ground_view)
        self.update()

    def create_dock_widgets(self):
        """Create docked error log"""
        self.error_log = ErrorLogWidget()
        error_dock = QDockWidget("System Errors", self)
        error_dock.setWidget(self.error_log)
        self.addDockWidget(Qt.BottomDockWidgetArea, error_dock)

    def connect_signals(self):
        """Connect data signals"""
        self.data_simulator.data_updated.connect(self.handle_data_update)
        self.btn_arm.clicked.connect(self.toggle_arm_state)
        self.btn_logging.clicked.connect(self.toggle_logging)
        self.data_simulator.start()

    def handle_data_update(self, data):
        """Handle incoming telemetry data"""
        current_view = self.ground_view if self.view_stack.currentIndex() == 0 else self.flight_view
        current_view.update_data(data)
        
        # Log errors
        if data['errors']['code'] is not None:
            self.error_log.add_entry(data['errors'])
        
        # Update status label
        status_text = "ARMED" if data['arm_status'] else "DISARMED"
        status_color = "#4CAF50" if data['arm_status'] else "#F44336"
        self.status_label.setText(f"STATUS: {status_text}")
        self.status_label.setStyleSheet(f"color: {status_color}; font: bold 14px;")
        
        # Log data
        if self.logger.logging:
            self.logger.log(data)

    def toggle_arm_state(self):
        """Toggle drone arm state"""
        current_state = self.data_simulator.armed
        self.data_simulator.armed = not current_state
        self.btn_arm.setText("DISARM" if not current_state else "ARM")

    def toggle_logging(self):
        """Toggle data logging state"""
        if self.logger.logging:
            self.logger.stop()
            self.btn_logging.setText("START LOGGING")
            self.btn_logging.setStyleSheet("""
                QPushButton {
                    min-width: 120px;
                    padding: 8px;
                    border-radius: 5px;
                    font: bold 12px;
                    background-color: #9C27B0;
                    color: white;
                }
            """)
        else:
            self.logger.start()
            self.btn_logging.setText("STOP LOGGING")
            self.btn_logging.setStyleSheet("""
                QPushButton {
                    min-width: 120px;
                    padding: 8px;
                    border-radius: 5px;
                    font: bold 12px;
                    background-color: #FF9800;
                    color: white;
                }
            """)

    def closeEvent(self, event):
        """Cleanup on window close"""
        self.data_simulator.stop()
        self.logger.stop()
        event.accept()
