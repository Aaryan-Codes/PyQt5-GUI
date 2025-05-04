from PyQt5.QtWidgets import (QGroupBox, QGridLayout, QLabel, QWidget, 
                            QHBoxLayout, QVBoxLayout, QFrame)
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPen, QPixmap
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtProperty, QPropertyAnimation, QEasingCurve, QRectF

class CoordinateIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(30, 30)
        self.setMaximumSize(30, 30)
        self._value_changed = False
        self._animation_timer = QTimer(self)
        self._animation_timer.timeout.connect(self._reset_highlight)
        self._color = QColor(30, 144, 255)  # Default blue
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw the coordinate indicator
        pen = QPen(self._color, 2)
        painter.setPen(pen)
        
        # Draw a compass-like indicator
        center_x = self.width() / 2
        center_y = self.height() / 2
        radius = min(center_x, center_y) - 2
        
        # Draw circle - using QRectF to handle float values
        rect = QRectF(center_x - radius, center_y - radius, radius * 2, radius * 2)
        painter.drawEllipse(rect)
        
        # Draw crosshairs - convert to int for drawLine
        painter.drawLine(int(center_x), int(center_y - radius), 
                         int(center_x), int(center_y + radius))
        painter.drawLine(int(center_x - radius), int(center_y), 
                         int(center_x + radius), int(center_y))
        
    def highlight_change(self):
        self._value_changed = True
        self._color = QColor(255, 165, 0)  # Orange for highlight
        self._animation_timer.start(800)  # Reset after 800ms
        self.update()
        
    def _reset_highlight(self):
        self._value_changed = False
        self._color = QColor(30, 144, 255)  # Back to blue
        self._animation_timer.stop()
        self.update()

class ValueLabel(QWidget):
    def __init__(self, initial_text="− − −"):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create the main value label
        self.value_label = QLabel(initial_text)
        self.value_label.setFont(QFont('Monospace', 12, QFont.Bold))
        self.value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.value_label.setStyleSheet("color: #FFFFFF;")
        
        # Create a frame for the value with a subtle background
        value_frame = QFrame()
        value_frame.setFrameShape(QFrame.StyledPanel)
        value_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 20, 40, 0.3);
                border-radius: 3px;
                padding: 2px;
            }
        """)
        value_layout = QHBoxLayout(value_frame)
        value_layout.setContentsMargins(5, 2, 5, 2)
        value_layout.addWidget(self.value_label)
        
        # Add the indicator and value frame to the layout
        self.indicator = CoordinateIndicator()
        layout.addWidget(self.indicator)
        layout.addWidget(value_frame, 1)
        
    def setText(self, text):
        current = self.value_label.text()
        if current != text:
            self.indicator.highlight_change()
        self.value_label.setText(text)

class PositionWidget(QGroupBox):
    def __init__(self):
        super().__init__("Position & Altitude")
        self.setStyleSheet("""
            QGroupBox {
                border: 2px solid #1E90FF;
                border-radius: 5px;
                margin-top: 1ex;
                font-weight: bold;
                color: #1E90FF;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                background-color: #0A1520;
            }
            QLabel {
                font: bold 12px;
                color: #D4D4D4;
            }
            QLabel.unit {
                color: #888888;
                font-size: 10px;
                font-style: italic;
            }
        """)
        
        main_layout = QVBoxLayout()
        
        # Create the position display grid
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setVerticalSpacing(8)
        
        # Create custom value labels
        self.lat_label = ValueLabel()
        self.lon_label = ValueLabel()
        self.alt_label = ValueLabel()
        
        # Create and configure the title labels with left alignment
        lat_title = QLabel("Latitude:")
        lat_title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        lon_title = QLabel("Longitude:")
        lon_title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        alt_title = QLabel("Altitude:")
        alt_title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # Create unit labels
        lat_unit = QLabel("deg")
        lat_unit.setProperty("class", "unit")
        lon_unit = QLabel("deg")
        lon_unit.setProperty("class", "unit")
        alt_unit = QLabel("meters")
        alt_unit.setProperty("class", "unit")
        
        # Add widgets to layout with proper alignment
        grid_layout.addWidget(lat_title, 0, 0)
        grid_layout.addWidget(self.lat_label, 0, 1)
        grid_layout.addWidget(lat_unit, 0, 2)
        
        grid_layout.addWidget(lon_title, 1, 0)
        grid_layout.addWidget(self.lon_label, 1, 1)
        grid_layout.addWidget(lon_unit, 1, 2)
        
        grid_layout.addWidget(alt_title, 2, 0)
        grid_layout.addWidget(self.alt_label, 2, 1)
        grid_layout.addWidget(alt_unit, 2, 2)
        
        # Set column stretch to ensure proper alignment
        grid_layout.setColumnStretch(0, 1)  # Title column
        grid_layout.setColumnStretch(1, 3)  # Value column
        grid_layout.setColumnStretch(2, 0)  # Unit column
        
        # Create a simple position indicator
        self.position_indicator = QWidget()
        self.position_indicator.setMinimumHeight(60)
        self.position_indicator.setStyleSheet("background-color: rgba(0, 20, 40, 0.3); border-radius: 3px;")
        
        # Add a paintEvent to the position indicator
        def paintEvent(event):
            painter = QPainter(self.position_indicator)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Draw a simple grid
            pen = QPen(QColor(60, 100, 140), 1, Qt.DotLine)
            painter.setPen(pen)
            
            w = self.position_indicator.width()
            h = self.position_indicator.height()
            
            # Draw grid lines
            for i in range(1, 5):
                painter.drawLine(0, h * i // 5, w, h * i // 5)
                painter.drawLine(w * i // 5, 0, w * i // 5, h)
            
            # Draw position marker
            pen.setColor(QColor(30, 144, 255))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(QBrush(QColor(30, 144, 255, 100)))
            
            # Position will be updated in update_data method
            # Use QRectF for the ellipse to handle float values
            painter.drawEllipse(QRectF(w // 2 - 5, h // 2 - 5, 10, 10))
            
            # Draw N/S/E/W indicators
            painter.setPen(QColor(200, 200, 200))
            painter.drawText(w // 2 - 5, 12, "N")
            painter.drawText(w // 2 - 5, h - 5, "S")
            painter.drawText(5, h // 2 + 5, "W")
            painter.drawText(w - 15, h // 2 + 5, "E")
        
        self.position_indicator.paintEvent = paintEvent
        
        # Add layouts to main layout
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.position_indicator)
        
        self.setLayout(main_layout)
        
        # Store last values for animation
        self._last_lat = 0
        self._last_lon = 0
        self._last_alt = 0

    def update_data(self, lat, lon, alt):
        # Update the labels with formatted values
        self.lat_label.setText(f"{lat:.6f}°")
        self.lon_label.setText(f"{lon:.6f}°")
        self.alt_label.setText(f"{alt:.1f}")
        
        # Store values for position indicator
        self._last_lat = lat
        self._last_lon = lon
        self._last_alt = alt
        
        # Update the position indicator
        self.position_indicator.update()
