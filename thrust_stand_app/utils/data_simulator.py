from PyQt5.QtCore import QObject, QTimer, pyqtSignal
import random
import math

class DataSimulator(QObject):
    data_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.base_rpm = 0
        self._running = False
        
        # Initial conditions
        self.voltage = 24.0  # Battery voltage
        self.temp = 25.0     # Starting temperature
        self.last_data = {}  # Store previous values for realistic transitions
        
        # System characteristics
        self.max_rpm = 12000
        self.voltage_drop_factor = 0.0002  # Voltage drop per RPM
        self.temp_rise_factor = 0.001      # Temperature rise per amp

    def start(self, interval=100):
        self._running = True
        self.timer.timeout.connect(self.generate_data)
        self.timer.start(interval)

    def stop(self):
        self._running = False
        self.timer.stop()
        # Reset values when stopped
        self.temp = 25.0
        self.voltage = 24.0

    def generate_data(self):
        # Calculate RPM with realistic fluctuation (smaller at lower RPMs)
        rpm_fluctuation = max(10, int(self.base_rpm * 0.02))
        actual_rpm = max(0, self.base_rpm + random.randint(-rpm_fluctuation, rpm_fluctuation))
        
        # Calculate current based on RPM (quadratic relationship)
        # Higher RPM = higher current draw
        rpm_ratio = actual_rpm / self.max_rpm
        base_current = 0.5 + (rpm_ratio ** 2) * 15  # 0.5A at idle, up to ~15.5A at max
        current = base_current + random.uniform(-0.2, 0.2)  # Small fluctuation
        
        # Calculate torque based on RPM and current
        # Torque is roughly proportional to current
        torque_factor = 0.3  # Nm per amp
        torque = current * torque_factor * (1 + random.uniform(-0.05, 0.05))
        
        # Update voltage (drops under load)
        self.voltage = max(18.0, 24.0 - (actual_rpm * self.voltage_drop_factor))
        voltage = self.voltage + random.uniform(-0.1, 0.1)  # Small fluctuation
        
        # Update temperature (rises with current draw, slowly)
        if self._running:
            # Temperature rises with current and time
            self.temp = min(85.0, self.temp + (current * self.temp_rise_factor))
        else:
            # Temperature falls when not running
            self.temp = max(25.0, self.temp - 0.1)
            
        temp = self.temp + random.uniform(-0.2, 0.2)  # Small fluctuation
        
        data = {
            'rpm': int(actual_rpm),
            'current': round(current, 2),
            'torque': round(torque, 2),
            'temp': round(temp, 1),
            'voltage': round(voltage, 2)
        }
        
        self.last_data = data
        self.data_updated.emit(data)

    def set_rpm(self, value):
        # Ensure RPM is within realistic bounds
        self.base_rpm = max(0, min(self.max_rpm, value))
