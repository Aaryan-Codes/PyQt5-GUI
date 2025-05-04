import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QMainWindow, 
                            QSplitter,QPushButton, QTabWidget, QStyleFactory, QLabel, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from widgets.live_view.chart_container import ChartContainer
from widgets.live_view.metrics_panel import MetricsPanel
from widgets.command_station.manual_control import ManualControl
from widgets.command_station.profile_control import ProfileControl, ProfileWorker
from utils.data_simulator import DataSimulator
from widgets.data_logging import DataLogging
from widgets.command_station.replay_control import ReplayControl

class ThrustStandApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_simulator = DataSimulator()
        self.set_application_style()
        self.init_ui()
        # self.data_simulator.start(100)
        # self.data_simulator.data_updated.connect(self.handle_data)

    def set_application_style(self):
        """Set the application style and color scheme"""
        # Set the application style to Fusion for a modern look
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        
        # Create a modern light palette with high contrast
        palette = QPalette()
        
        # Main colors - light theme with good contrast
        background_color = QColor("#f5f7fa")
        text_color = QColor("#2d3436")
        accent_color = QColor("#0984e3")
        secondary_bg = QColor("#ffffff")
        panel_bg = QColor("#e9ecef")
        
        # Set color roles
        palette.setColor(QPalette.Window, background_color)
        palette.setColor(QPalette.WindowText, text_color)
        palette.setColor(QPalette.Base, secondary_bg)
        palette.setColor(QPalette.AlternateBase, panel_bg)
        palette.setColor(QPalette.ToolTipBase, text_color)
        palette.setColor(QPalette.ToolTipText, secondary_bg)
        palette.setColor(QPalette.Text, text_color)
        palette.setColor(QPalette.Button, panel_bg)
        palette.setColor(QPalette.ButtonText, text_color)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, accent_color)
        palette.setColor(QPalette.Highlight, accent_color)
        palette.setColor(QPalette.HighlightedText, secondary_bg)
        
        # Apply the palette
        QApplication.setPalette(palette)

    def init_ui(self):
        self.setWindowTitle("Sarla Aviation - Thrust Stand Controller")
        self.setGeometry(100, 100, 1600, 900)
        
        # Main container
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Create a header with title
        header = QFrame()
        header.setFrameShape(QFrame.StyledPanel)
        header.setStyleSheet("""
            QFrame {
                background-color: #0984e3;
                border-radius: 8px;
                border: none;
            }
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(15, 10, 15, 10)
        
        title_label = QLabel("THRUST STAND CONTROLLER")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; letter-spacing: 1px;font-size: 18px;")
        header_layout.addWidget(title_label)
        
        # Main content area
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(15)
        
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setHandleWidth(1)
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #dfe6e9;
            }
        """)
        
        # Left Panel - Charts and Metrics
        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.StyledPanel)
        left_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #dfe6e9;
            }
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(15)
        
        # Chart container with shadow effect
        self.chart_container = ChartContainer(self.data_simulator)
        self.chart_container.setStyleSheet("""
            background-color: white;
            border-radius: 8px;
            border: 1px solid #dfe6e9;
            
            /* Fix for capture graph button */
            QPushButton[objectName="captureGraphBtn"] {
                background-color: #00b894;
                color: #000000;
                font-weight: bold;
                font-size: 11pt;
                padding: 8px 16px;
                border-radius: 4px;
            }
            
            QPushButton[objectName="captureGraphBtn"]:hover {
                background-color: #00a885;
            }
            
            QPushButton[objectName="captureGraphBtn"]:pressed {
                background-color: #009876;
            }
        """)
        
        # Connect the chart visibility toggle signals
        # This ensures the chart only displays selected data series
        if hasattr(self.chart_container, 'series_visibility_changed'):
            self.chart_container.series_visibility_changed.connect(self.update_chart_visibility)
        
        # Metrics panel with shadow effect
        self.metrics_panel = MetricsPanel()
        self.metrics_panel.setStyleSheet("""
            background-color: white;
            border-radius: 8px;
            border: 1px solid #dfe6e9;
        """)
        
        left_layout.addWidget(self.chart_container, 70)
        left_layout.addWidget(self.metrics_panel, 30)
        
        # Right Panel - Controls
        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.StyledPanel)
        right_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #dfe6e9;
            }
        """)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(15, 15, 15, 15)
        
        self.manual_control = ManualControl(self.data_simulator)
        self.profile_control = ProfileControl(self.handle_profile_data)
        self.replay_control = ReplayControl(self.data_simulator)
        self.data_logging = DataLogging(self.data_simulator)
        
        # Modern tab widget styling with improved visibility for tab names
        right_tabs = QTabWidget()
        right_tabs.setStyleSheet("""
            QTabWidget::pane { 
                border: none;
                background-color: white; 
                border-radius: 8px; 
            }
            QTabBar::tab { 
                background-color: #f1f2f6; 
                color: #2d3436; 
                padding: 10px 20px; 
                margin-right: 4px; 
                border-top-left-radius: 6px; 
                border-top-right-radius: 6px; 
                font-weight: 500;
                border: 1px solid #dfe6e9;
                border-bottom: none;
                min-width: 120px; /* Ensure tabs have enough width */
                max-width: 200px; /* Limit maximum width */
            }
            QTabBar::tab:selected { 
                background-color: #0984e3; 
                color: white; 
                border: 1px solid #0984e3;
                border-bottom: none;
            }
            QTabBar::tab:hover:!selected { 
                background-color: #dfe6e9; 
            }
        """)
        
        right_tabs.addTab(self.manual_control, "Manual Control")
        right_tabs.addTab(self.profile_control, "Profile Control")
        right_tabs.addTab(self.replay_control, "Replay Data")
        right_tabs.addTab(self.data_logging, "Data Logging")
        
        right_layout.addWidget(right_tabs)
        
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([1000, 600])
        
        content_layout.addWidget(main_splitter)
        
        # Add components to main layout
        main_layout.addWidget(header, 1)
        main_layout.addWidget(content, 9)
        
        # Set global widget styles
        qss = """
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #0984e3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0878d4;
            }
            QPushButton:pressed {
                background-color: #076ebf;
            }
            QPushButton:disabled {
                background-color: #b2bec3;
                color: #636e72;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 6px;
                border: 1px solid #dfe6e9;
                border-radius: 4px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #dfe6e9;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #0984e3;
                width: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: #74b9ff;
                border-radius: 4px;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dfe6e9;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            /* Style for data series selection checkboxes */
            QCheckBox {
                spacing: 8px;
                font-weight: 500;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 1px solid #dfe6e9;
            }
            QCheckBox::indicator:checked {
                background-color: #0984e3;
                border: 1px solid #0984e3;
                image: url(check.png);
            }
            QCheckBox::indicator:unchecked {
                background-color: white;
            }
        """
        self.setStyleSheet(qss)
        
        # After setting up the UI, find and explicitly style the capture graph button
        # self.find_and_style_capture_button()
        
        self.setCentralWidget(main_widget)
        self.metrics_panel.connect_to_simulator(self.data_simulator)
        self.data_simulator.start(100)
        # self.data_simulator.data_updated.connect(self.handle_data)

    def handle_data(self, data):
        # Update visualization components
        self.chart_container.update_charts(data)
        self.metrics_panel.update_metrics(data)
        
        # Handle data logging
        if self.data_logging.logging_active:
            self.data_logging.log_data(data)

    def handle_profile_data(self, rpm):
        self.data_simulator.set_rpm(rpm)
        
    def update_chart_visibility(self, series_name, visible):
        # Update the chart to show only selected series
        if hasattr(self.chart_container, 'set_series_visibility'):
            self.chart_container.set_series_visibility(series_name, visible)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThrustStandApp()
    window.show()
    sys.exit(app.exec_())
