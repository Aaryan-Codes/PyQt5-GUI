from PyQt5.QtCore import QThread, pyqtSignal
import random
import time
import math

class DataSimulator(QThread):
    data_updated = pyqtSignal(dict)
    
    def __init__(self, interval=1):
        super().__init__()
        self.running = True
        self.interval = interval # in seconds
        
        # Initial GPS state
        self.lat = 13.0000
        self.lon = 77.6000
        self.alt = 150.0
        
        # Flight dynamics
        self.heading = random.uniform(0, 360)  # degrees
        self.speed = 0.0  # m/s
        self.max_speed = 15.0  # m/s
        self.acceleration = 0.2  # m/s²
        
        # Attitude
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = self.heading
        
        # System state
        self.armed = False
        self.motor_rpms = [0] * 7
        self.motor_temps = [ambient_temp() for _ in range(7)]
        self.battery_levels = [100.0] * 4
        self.battery_temps = [ambient_temp() for _ in range(4)]
        
        # Sensor health - more realistic to start with all healthy
        self.sensor_health = {
            'IMU': 1,
            'Altimeter': 1,
            'Magnetometer': 1,
            'PitotTube': 1
        }
        
        # Error probability decreases
        self.error_probability = 0.02
        
        # Time tracking for realistic changes
        self.time_elapsed = 0
        
    def run(self):
        while self.running:
            self._update_flight_dynamics()
            data = self._generate_data()
            self.data_updated.emit(data)
            time.sleep(self.interval)
            self.time_elapsed += self.interval
            
    def stop(self):
        self.running = False
        self.quit()
        self.wait()
    
    def _update_flight_dynamics(self):
        # Simulate realistic flight behavior
        
        # Random heading changes (smoother turns)
        if random.random() < 0.1:
            heading_change = random.uniform(-5, 5)
            self.heading = (self.heading + heading_change) % 360
            # Bank into turns
            self.roll = heading_change * 2
        else:
            # Gradually return to level flight
            self.roll = self.roll * 0.9
        
        # Speed changes
        if not self.armed and random.random() < 0.05:
            self.armed = True
        
        if self.armed:
            if self.speed < self.max_speed and random.random() < 0.7:
                self.speed = min(self.max_speed, self.speed + self.acceleration)
            elif random.random() < 0.1:
                self.speed = max(0, self.speed - self.acceleration)
        else:
            self.speed = max(0, self.speed - self.acceleration)
        
        # Convert heading and speed to lat/lon changes
        # Approximate conversion (not accounting for Earth's curvature for simplicity)
        heading_rad = math.radians(self.heading)
        lat_change = self.speed * math.cos(heading_rad) * 0.00001
        lon_change = self.speed * math.sin(heading_rad) * 0.00001
        
        self.lat += lat_change
        self.lon += lon_change
        
        # Altitude changes (smoother)
        if random.random() < 0.1:
            self.alt += random.uniform(-2, 2)
            # Pitch follows altitude changes
            self.pitch = (self.alt - 150) * 0.1
        else:
            # Gradually return to neutral pitch
            self.pitch = self.pitch * 0.9
        
        # Update yaw to match heading
        self.yaw = self.heading
        
        # Update motor RPMs based on speed and maneuvers
        base_rpm = 3000 + (self.speed / self.max_speed) * 5000
        for i in range(7):
            # Add some variation between motors
            self.motor_rpms[i] = int(base_rpm + random.uniform(-200, 200))
        
        # Update motor temperatures based on RPMs and time
        for i in range(7):
            rpm_factor = self.motor_rpms[i] / 8000  # Normalized RPM
            # Temperature rises with RPM and time, but has a cooling factor
            temp_change = (rpm_factor * 0.5) - 0.1
            self.motor_temps[i] = min(95, max(ambient_temp(), self.motor_temps[i] + temp_change))
        
        # Battery levels decrease over time when armed
        if self.armed:
            for i in range(4):
                # Drain rate depends on motor RPMs
                drain_rate = 0.02 * (sum(self.motor_rpms) / (7 * 8000))
                self.battery_levels[i] = max(0, self.battery_levels[i] - drain_rate)
                
                # Battery temperature rises with use
                self.battery_temps[i] = min(75, self.battery_temps[i] + 0.05 * drain_rate)
        else:
            # Batteries cool down when not in use
            for i in range(4):
                self.battery_temps[i] = max(ambient_temp(), self.battery_temps[i] - 0.1)
        
    def _generate_data(self):
        # GPS health improves with time but occasionally degrades
        satellites = min(20, 10 + int(self.time_elapsed / 60))
        if random.random() < 0.05:
            satellites = max(6, satellites - random.randint(1, 3))
        
        hdop = max(0.5, 2.0 - (satellites / 20))
        pdop = hdop + random.uniform(0, 0.5)
        
        return {
            'motor_rpms': self.motor_rpms,
            'motor_temps': self.motor_temps,
            'latitude': self.lat, 
            'longitude': self.lon,
            'altitude': self.alt,
            'roll': self.roll,
            'pitch': self.pitch,
            'yaw': self.yaw,
            'battery_levels': self.battery_levels,
            'battery_temps': self.battery_temps,
            'arm_status': self.armed,
            'gps_health': {
                'HDOP': round(hdop, 2),
                'PDOP': round(pdop, 2),
                'satellites': satellites
            },
            'sensor_health': self._update_sensor_health(),
            'errors': self._generate_errors() or {
                'code': None,
                'desc': None,
                'source': None
            }
        }
    
    def _update_sensor_health(self):
        # Sensors occasionally fail but can recover
        for sensor in self.sensor_health:
            if self.sensor_health[sensor] == 1 and random.random() < 0.01:
                self.sensor_health[sensor] = 0
            elif self.sensor_health[sensor] == 0 and random.random() < 0.05:
                self.sensor_health[sensor] = 1
        
        return self.sensor_health
        
    def _generate_errors(self):
        # Errors are more likely when:
        # - Motors are running hot
        # - Batteries are low
        # - Sensors are failing
        
        # Check for motor overheat
        if any(temp > 90 for temp in self.motor_temps) and random.random() < 0.3:
            return {
                'code': "E101",
                'desc': "Motor Overheat",
                'source': "Motors"
            }
        
        # Check for battery issues
        if any(level < 30 for level in self.battery_levels) and random.random() < 0.3:
            return {
                'code': "E102",
                'desc': "Battery Undervoltage",
                'source': "Battery"
            }
        
        # Check for sensor failures
        if 0 in self.sensor_health.values() and random.random() < 0.3:
            failed_sensor = next(s for s, v in self.sensor_health.items() if v == 0)
            return {
                'code': f"E{103 + list(self.sensor_health.keys()).index(failed_sensor)}",
                'desc': f"{failed_sensor} Failure",
                'source': "Flight Controller"
            }
        
        # Random errors with lower probability
        if random.random() < self.error_probability:
            return {
                'code': f"E{random.randint(101, 199)}",
                'desc': random.choice([
                    "Motor Overheat", "Battery Undervoltage", "IMU Failure", "GPS Lost"
                ]),
                'source': random.choice(["Motors", "Battery", "Flight Controller"])
            }
        return None

def ambient_temp():
    """Return a realistic ambient temperature"""
    return random.uniform(25, 30)
