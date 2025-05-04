from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QVBoxLayout
from widgets.attitude_widget import AttitudeWidget
from widgets.system_widget import SystemWidget
from widgets.motor_widget import MotorWidget
from widgets.battery_widget import BatteryWidget
from widgets.map_widget import MapWidget
from widgets.gps_widget import GPSWidget
from widgets.sensor_widget import SensorWidget
from widgets.position_widget import PositionWidget

class FlightView(QWidget):
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
        
        # Row 0: Flight Instruments (Top priority during flight)
        self.attitude = AttitudeWidget()
        self.system = SystemWidget()
        self.grid.addWidget(self.attitude, 0, 0)
        self.grid.addWidget(self.system, 0, 1)
        
        # Row 1: Position/Altitude (Critical during flight)
        self.position = PositionWidget()
        self.sensors = SensorWidget()
        self.grid.addWidget(self.position, 1, 0)
        self.grid.addWidget(self.sensors, 1, 1)
        
        # Row 2: Map (Important for navigation)
        self.map = MapWidget()
        self.grid.addWidget(self.map, 2, 0, 1, 2)  # Span full width
        
        # Row 3: Power Systems (Monitoring during flight)
        self.batteries = BatteryWidget()
        self.motors = MotorWidget()
        self.grid.addWidget(self.batteries, 3, 0)
        self.grid.addWidget(self.motors, 3, 1)
        
        # Row 4: GPS
        self.gps = GPSWidget()
        self.grid.addWidget(self.gps, 4, 0, 1, 2)
        
        # Configure grid proportions - different priorities for flight
        self.grid.setRowStretch(0, 3)  # Flight instruments get most space
        self.grid.setRowStretch(1, 2)  # Position/sensors
        self.grid.setRowStretch(2, 2)  # Map
        self.grid.setRowStretch(3, 1)  # Power systems
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
        
        # Flight mode is more prominent in flight view
        self.system.update_status(
            data['arm_status'],
            data.get('flight_mode', "STABILIZE"),
            data['gps_health']['satellites'],
            data.get('rc_connected', True)
        )
        
        self.position.update_data(
            data['latitude'], 
            data['longitude'], 
            data['altitude']
        )
        
        self.sensors.update_status(data['sensor_health'])
        
        self.batteries.update_data(
            data['battery_levels'], 
            data['battery_temps']
        )
        
        self.motors.update_data(
            data['motor_rpms'], 
            data['motor_temps']
        )
        
        self.gps.update_data(data['gps_health'])
        
        self.map.update_position(
            data['latitude'], 
            data['longitude']
        )
