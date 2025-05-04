from PyQt5.QtWidgets import QTabWidget, QWidget, QGridLayout, QLabel
from PyQt5.QtCore import pyqtSlot

class MetricsPanel(QTabWidget):
    def __init__(self):
        super().__init__()
        self.init_metrics_tab()
        self.init_details_tab()

    def init_metrics_tab(self):
        widget = QWidget()
        grid = QGridLayout()
        
        # Primary Metrics
        metrics = [
            ("RPM", "5", "rpm_label"),
            ("Current", "0 A", "current_label"),
            ("Temperature", "0°C", "temp_label"),
            ("Voltage", "0 V", "voltage_label"),
            ("Torque", "0 Nm", "torque_label"),
            ("Thrust", "0 N", "thrust_label")
        ]
        
        for row, (label, value, obj_name) in enumerate(metrics):
            grid.addWidget(QLabel(f"{label}:"), row, 0)
            value_label = QLabel(value)
            value_label.setObjectName(obj_name)
            grid.addWidget(value_label, row, 1)
            
        widget.setLayout(grid)
        self.addTab(widget, "Metrics")
        
    def update_metrics(self, data):
        # Update metric labels with defensive checks
        rpm = self.findChild(QLabel, "rpm_label")
        temp = self.findChild(QLabel, "temp_label")
        current = self.findChild(QLabel, "current_label")
        voltage = self.findChild(QLabel, "voltage_label")
        torque = self.findChild(QLabel, "torque_label")
        thrust = self.findChild(QLabel, "thrust_label")
        
        if rpm and 'rpm' in data:
            rpm.setText(f"{data['rpm']:.0f}")
        if temp and ('temp' in data or 'temperature' in data):
            temp_value = data.get('temp', data.get('temperature', 0))
            temp.setText(f"{temp_value:.1f}°C")
        if current and 'current' in data:
            current.setText(f"{data['current']:.2f} A")
        if voltage and 'voltage' in data:
            voltage.setText(f"{data['voltage']:.1f} V")
        if torque and 'torque' in data:
            torque.setText(f"{data['torque']:.2f} Nm")
        if thrust and 'thrust' in data:
            thrust.setText(f"{data['thrust']:.1f} N")

    def init_details_tab(self):
        widget = QWidget()
        layout = QGridLayout()
        
        # Performance Metrics
        perf_metrics = [
            ("Efficiency", "0 g/W", "efficiency_label"), 
            ("Power", "0 W", "power_label"), 
            ("Thrust/Weight", "0", "thrust_weight_label")
        ]
        
        # System Status
        sys_metrics = [
            ("Data Rate", "0 Hz", "data_rate_label"), 
            ("Connection", "Stable", "connection_label"), 
            ("Latency", "0 ms", "latency_label")
        ]
        
        for idx, (label, value, obj_name) in enumerate(perf_metrics):
            layout.addWidget(QLabel(f"{label}:"), idx, 0)
            value_label = QLabel(value)
            value_label.setObjectName(obj_name)
            layout.addWidget(value_label, idx, 1)
            
        for idx, (label, value, obj_name) in enumerate(sys_metrics):
            layout.addWidget(QLabel(f"{label}:"), idx, 2)
            value_label = QLabel(value)
            value_label.setObjectName(obj_name)
            layout.addWidget(value_label, idx, 3)
            
        widget.setLayout(layout)
        self.addTab(widget, "Details")

    def update_details(self, data):
        # Update performance metrics
        efficiency = self.findChild(QLabel, "efficiency_label")
        power = self.findChild(QLabel, "power_label")
        thrust_weight = self.findChild(QLabel, "thrust_weight_label")
        
        # System status metrics
        data_rate = self.findChild(QLabel, "data_rate_label")
        connection = self.findChild(QLabel, "connection_label")
        latency = self.findChild(QLabel, "latency_label")
        
        # Calculate derived metrics from raw data
        if 'current' in data and 'voltage' in data:
            power_value = data['current'] * data['voltage']
            if power and power_value:
                power.setText(f"{power_value:.2f} W")
                
            # Calculate efficiency if thrust is available
            if 'thrust' in data and power_value > 0:
                # Convert thrust from N to g (1N ≈ 102g)
                thrust_g = data['thrust'] * 102
                efficiency_value = thrust_g / power_value
                if efficiency:
                    efficiency.setText(f"{efficiency_value:.2f} g/W")
        
        # Update thrust/weight ratio (assuming a fixed motor weight for now)
        motor_weight_n = 0.5  # Example fixed motor weight in Newtons
        if 'thrust' in data and motor_weight_n > 0:
            tw_ratio = data['thrust'] / motor_weight_n
            if thrust_weight:
                thrust_weight.setText(f"{tw_ratio:.2f}")
        
        # Update system status metrics with defensive checks
        if data_rate:
            data_rate.setText("10.0 Hz")  # Fixed rate based on simulator interval
        if connection:
            connection.setText("Simulated")
        if latency:
            latency.setText("5 ms")  # Simulated latency
            
    def connect_to_chart(self, chart_container):
        """Connect this metrics panel to a chart container to receive data updates"""
        chart_container.data_sync_signal.connect(self.update_from_chart)
        
    def update_from_chart(self, data):
        """Update both metrics and details panels from chart data"""
        self.update_metrics(data)
        self.update_details(data)
        
    def connect_to_simulator(self, simulator):
        """Connect this metrics panel to a data simulator to receive updates"""
        simulator.data_updated.connect(self.update_from_simulator)
        
    @pyqtSlot(dict)
    def update_from_simulator(self, data):
        """Update both metrics and details panels from simulator data"""
        # Calculate thrust based on torque and RPM (simplified model)
        if 'torque' in data and 'rpm' in data:
            # Simple thrust calculation: torque * rpm / constant
            # This is a simplified model - real thrust calculations would be more complex
            data['thrust'] = data['torque'] * data['rpm'] / 100
            
        self.update_metrics(data)
        self.update_details(data)
