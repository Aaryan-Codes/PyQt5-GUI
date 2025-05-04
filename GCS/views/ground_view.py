from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QVBoxLayout
from widgets.attitude_widget import AttitudeWidget
from widgets.system_widget import SystemWidget
from widgets.motor_widget import MotorWidget
from widgets.battery_widget import BatteryWidget
from widgets.map_widget import MapWidget
from widgets.gps_widget import GPSWidget
from widgets.sensor_widget import SensorWidget
from widgets.position_widget import PositionWidget

class GroundView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Create scroll area for responsive layout
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Main content widget
        content = QWidget()
        self.grid = QGridLayout(content)
        
        # Row 0: Map (Top priority position)
        self.map = MapWidget()
        self.grid.addWidget(self.map, 0, 0, 1, 2)  # Span full width

        # Row 1: Flight Instruments
        self.attitude = AttitudeWidget()
        self.system = SystemWidget()
        self.grid.addWidget(self.attitude, 1, 0)
        self.grid.addWidget(self.system, 1, 1)

        # Row 2: Power Systems
        self.motors = MotorWidget()
        self.batteries = BatteryWidget()
        self.grid.addWidget(self.motors, 2, 0)
        self.grid.addWidget(self.batteries, 2, 1)

        # Row 3: Position/Sensors
        self.position = PositionWidget()
        self.sensors = SensorWidget()
        self.grid.addWidget(self.position, 3, 0)
        self.grid.addWidget(self.sensors, 3, 1)

        # Row 4: GPS
        self.gps = GPSWidget()
        self.grid.addWidget(self.gps, 4, 0, 1, 2)

        # Configure grid proportions
        self.grid.setRowStretch(0, 3)  # Map gets most space
        self.grid.setRowStretch(1, 1)  # Flight instruments
        self.grid.setRowStretch(2, 1)  # Power systems
        self.grid.setRowStretch(3, 1)  # Position/sensors
        self.grid.setRowStretch(4, 1)  # GPS
        
        scroll.setWidget(content)
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def update_data(self, data):
        # Update all components with new telemetry data
        self.attitude.update_attitude(
            roll=data['roll'],
            pitch=data['pitch'],
            yaw=data.get('yaw', 0.0)
        )
        self.system.update_status(
            data['arm_status'],
            "STABILIZE",
            data['gps_health']['satellites'],
            True
        )
        self.motors.update_data(data['motor_rpms'], data['motor_temps'])
        self.batteries.update_data(data['battery_levels'], data['battery_temps'])
        self.position.update_data(data['latitude'], data['longitude'], data['altitude'])
        self.sensors.update_status(data['sensor_health'])
        self.gps.update_data(data['gps_health'])
        self.map.update_position(data['latitude'], data['longitude'])