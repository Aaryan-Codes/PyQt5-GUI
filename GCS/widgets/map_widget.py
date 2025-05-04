from PyQt5.QtWidgets import QWidget, QVBoxLayout,QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSlot
import os

class MapWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #252526;
                margin-top: 15px;
            }
            QLabel {
                font: bold 12px;
            }
        """)

        self.view = QWebEngineView()
        self.layout.addWidget(self.view)

        # Track if map is ready
        self.map_ready = False
        self.pending_position = None

        # Load the map HTML file
        
        map_path = os.path.join(os.path.dirname(__file__), "leaflet_map.html")
        map_path = os.path.abspath(map_path)

        print("[MapWidget] Loading:",map_path)
        self.view.setMinimumHeight(400)
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.view.load(QUrl.fromLocalFile(map_path))
        self.view.loadFinished.connect(self.on_map_loaded)

    @pyqtSlot(bool)
    def on_map_loaded(self, ok):
        if ok:
            self.map_ready = True
            if self.pending_position:
                self._send_position(*self.pending_position)
                self.pending_position = None

    def update_position(self, lat, lon):
        if self.map_ready:
            self._send_position(lat, lon)
        else:
            self.pending_position = (lat, lon)

    def _send_position(self, lat, lon):
        js_code = f"updatePosition({lat}, {lon});"
        self.view.page().runJavaScript(js_code)
