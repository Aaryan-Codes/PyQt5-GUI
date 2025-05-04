from PyQt5.QtWidgets import QWidget, QAbstractItemView, QPushButton, QListWidget, QVBoxLayout, QTabWidget, QComboBox, QHBoxLayout, QGridLayout
from PyQt5.QtCore import pyqtSignal
import pyqtgraph as pg
from pyqtgraph import PlotWidget
from datetime import datetime
from pyqtgraph.exporters import ImageExporter
import time

class ChartContainer(QWidget):
    # Signal to sync data with metrics panel
    data_sync_signal = pyqtSignal(dict)
    
    def __init__(self, data_simulator):
        super().__init__()
        self.data_simulator = data_simulator
        self.plot_data = {"x": [], "rpm": [], "current": [], "torque": [], "thrust": [], 
                         "temperature": [], "voltage": [], "temp": []}
        self.param_selector = QListWidget()
        self.init_ui()
        self.init_signals()
        self.add_controls()
        
    def add_controls(self):
        control_layout = QHBoxLayout()
        
        # Parameter selection with checkboxes
        self.param_selector = QListWidget()
        self.param_selector.setSelectionMode(QAbstractItemView.MultiSelection)
        self.param_selector.addItems(["RPM", "Current", "Torque", "Thrust", "Temperature", "Voltage"])
        self.param_selector.setMaximumHeight(100)
        
        # Screenshot button
        self.screenshot_btn = QPushButton("Capture Graph")
        self.screenshot_btn.setStyleSheet(
            """
                QPushButton{
                    background-color: #00b894;
                color: #ffffff;
                font-weight: bold;
                font-size: 11pt;
                padding: 8px 16px;
                border-radius: 4px;
                }
            """
        )
        self.screenshot_btn.clicked.connect(self.save_screenshot)
        
        control_layout.addWidget(self.param_selector)
        control_layout.addWidget(self.screenshot_btn)
        self.main_layout.insertLayout(0, control_layout)
        
    def save_screenshot(self, clicked=None):
        # Ignore the clicked parameter that comes from the button signal
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'chart_{timestamp}.png'
            
        # Get the current tab
        current_tab = self.view_tabs.currentWidget()
        if current_tab == self.single_chart_widget:
            exporter = ImageExporter(self.single_plot_widget.plotItem)
            exporter.export(filename)
            print(f"Screenshot saved as {filename}")
        elif current_tab == self.grid_view_widget:
            # For grid view, save the first plot as an example
            if self.plot_widgets:
                first_metric = list(self.plot_widgets.keys())[0]
                exporter = ImageExporter(self.plot_widgets[first_metric].plotItem)
                exporter.export(filename)
                print(f"Screenshot saved as {filename}")
        else:
            print("No valid widget to capture.")

            
    def init_ui(self):
        self.main_layout = QVBoxLayout()
        
        # Create tab widget
        self.view_tabs = QTabWidget()
        
        # Create single chart view
        self.single_chart_widget = QWidget()
        self.create_single_chart()
        
        # Create grid view
        self.grid_view_widget = QWidget()
        self.create_grid_view()
        
        # Add tabs
        self.view_tabs.addTab(self.single_chart_widget, "Single Chart")
        self.view_tabs.addTab(self.grid_view_widget, "Grid View")
        
        # Parameter selector for single view
        self.parameter_selector = QComboBox()
        self.parameter_selector.addItems(["All", "RPM", "Current", "Torque", "Thrust", "Temperature", "Voltage"])
        
        # Add widgets to layout
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.parameter_selector)
        self.main_layout.addLayout(control_layout)
        self.main_layout.addWidget(self.view_tabs)
        self.setLayout(self.main_layout)
        
    def create_single_chart(self):
        layout = QVBoxLayout()
        self.single_plot_widget = pg.PlotWidget(title="Live Motor Metrics")
        self.single_plot_widget.setBackground('w')
        self.single_plot_widget.addLegend()
        self.single_plot_widget.setLabel('left', 'Value')
        self.single_plot_widget.setLabel('bottom', 'Time')
        
        self.visible_params = {"RPM", "Current"}  # Default visible parameters
        
        # Create curves for single chart
        self.single_curves = {
            'RPM': self.single_plot_widget.plot(pen='r', name='RPM'),
            'Current': self.single_plot_widget.plot(pen='b', name='Current'),
            'Torque': self.single_plot_widget.plot(pen='g', name='Torque'),
            'Thrust': self.single_plot_widget.plot(pen='y', name='Thrust'),
            'Temperature': self.single_plot_widget.plot(pen='m', name='Temperature'),
            'Voltage': self.single_plot_widget.plot(pen=(0, 128, 0), name='Voltage')
        }
        
        layout.addWidget(self.single_plot_widget)
        self.single_chart_widget.setLayout(layout)
        
    def create_grid_view(self):
        grid_layout = QGridLayout()
        
        # Define metrics and their properties
        metrics = ['RPM', 'Current', 'Torque', 'Thrust', 'Temperature', 'Voltage']
        colors = ['r', 'b', 'g', 'y', 'm', (0, 128, 0)]
        
        self.plot_widgets = {}
        self.grid_curves = {}
        
        # Create a grid of plot widgets
        cols = 3
        for index, metric in enumerate(metrics):
            plot_widget = pg.PlotWidget(title=metric)
            plot_widget.setBackground('w')
            plot_widget.setLabel('left', metric)
            plot_widget.setLabel('bottom', 'Time')
            curve = plot_widget.plot(pen=colors[index])
            self.plot_widgets[metric] = plot_widget
            self.grid_curves[metric] = curve
            
            row = index // cols
            col = index % cols
            grid_layout.addWidget(plot_widget, row, col)
            
        self.grid_view_widget.setLayout(grid_layout)
        
    def init_signals(self):
        self.data_simulator.data_updated.connect(self.update_charts)
        self.parameter_selector.currentTextChanged.connect(self.update_visibility)
        self.param_selector.itemSelectionChanged.connect(self.update_param_visibility)
        
    def update_charts(self, data):
    # Add timestamp
        timestamp = len(self.plot_data['x'])
        self.plot_data['x'].append(timestamp)
        
        # Update data for each metric
        metrics = {
            'rpm': 'RPM',
            'current': 'Current',
            'torque': 'Torque',
            'thrust': 'Thrust',
            'temperature': 'Temperature',
            'voltage': 'Voltage'
        }
        
        # Create a dictionary to hold the data for syncing with metrics panel
        sync_data = {}
        
        # Add new data points
        for key, display_name in metrics.items():
            if key in data:
                # Ensure values are non-negative
                value = max(0, data[key])
                self.plot_data[key].append(value)
                sync_data[key] = value
                
                # Special case for temperature (both 'temperature' and 'temp' keys)
                if key == 'temperature':
                    self.plot_data['temp'].append(value)
                    sync_data['temp'] = value
            else:
                # If data doesn't have this key, append a default value
                self.plot_data[key].append(0)
        
        # Calculate derived metrics for details panel
        if 'thrust' in sync_data and 'power' in data:
            # Ensure power is positive to avoid division by zero
            power = max(data['power'], 0.1)
            # Efficiency in g/W (thrust in grams per watt)
            sync_data['efficiency'] = (sync_data['thrust'] * 102) / power  # Convert N to g and divide by power
        
        if 'current' in sync_data and 'voltage' in sync_data:
            # Power in watts
            sync_data['power'] = sync_data['current'] * sync_data['voltage']
            
        # Add thrust/weight ratio (assuming a fixed motor weight)
        if 'thrust' in sync_data:
            motor_weight_in_newtons = 0.5  # Example: 500g motor = 0.5N
            sync_data['thrust_weight'] = sync_data['thrust'] / motor_weight_in_newtons
            
        # Add system metrics
        sync_data['data_rate'] = max(0, data.get('data_rate', 10.0))  # Default to 10Hz
        sync_data['connection'] = data.get('connection', 'Stable')
        sync_data['latency'] = max(0, data.get('latency', 5))  # Default to 5ms
        
        # Emit the signal to sync with metrics panel
        self.data_sync_signal.emit(sync_data)
        
        # Limit data points but keep scrolling effect
        max_points = 100
        if len(self.plot_data['x']) > max_points:
            # Shift data instead of truncating to create scrolling effect
            for key in self.plot_data:
                self.plot_data[key] = self.plot_data[key][-max_points:]
                
            # Adjust x-axis values to maintain continuous scrolling
            min_x = min(self.plot_data['x'])
            self.plot_data['x'] = [x - min_x for x in self.plot_data['x']]
            
        # Update single chart view
        for key, display_name in metrics.items():
            self.single_curves[display_name].setData(self.plot_data['x'], self.plot_data[key])
            
        # Update grid view
        for key, display_name in metrics.items():
            if display_name in self.grid_curves:
                self.grid_curves[display_name].setData(self.plot_data['x'], self.plot_data[key])

                
    def update_visibility(self, selected):
        # For single chart view
        if selected == "All":
            for curve in self.single_curves.values():
                curve.show()
        else:
            for name, curve in self.single_curves.items():
                if name == selected:
                    curve.show()
                else:
                    curve.hide()
                    
    def update_param_visibility(self):
        # For parameter selector in controls
        selected_items = self.param_selector.selectedItems()
        selected_params = [item.text() for item in selected_items]
        
        # If no parameters selected, show all
        if not selected_params:
            for curve in self.single_curves.values():
                curve.show()
        else:
            for name, curve in self.single_curves.items():
                if name in selected_params:
                    curve.show()
                else:
                    curve.hide()
