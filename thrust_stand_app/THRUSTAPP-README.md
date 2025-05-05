## Thrust Stand Command Station - 📘 Overview

The **Thrust Stand Command Station** is a desktop application built using Python and PyQt5, designed to visualize and monitor telemetry from a thrust measurement setup. It provides engineers and operators with a real-time, intuitive interface to observe critical flight parameters such as RPM, current, voltage, thrust, and more.

Key features include:
- Real-time plotting of sensor data across multiple graphs
- A clean, modular layout that separates concerns for maintainability
- Simulated data playback and logging for development and testing
- Custom widgets for battery, GPS, motor info, and other telemetry panels

---

## 🧠 Design Decisions & Rationale

The following table outlines the major design choices made during development, along with the reasoning behind each:

| **Design Decision**         | **Chosen Approach**                                                        | **Rationale**                                                                 |
|-----------------------------|----------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| **Modular Widget Structure**| Separated into logical `QWidget` subclasses (e.g., `BatteryWidget`, `MotorWidget`) | Promotes reusability, clearer architecture, and easier debugging and enhancements. |
| **PyQt5 as Framework**      | Built entirely with PyQt5 and Qt Designer                                 | Offers cross-platform compatibility, responsive UI design, and robust signal-slot communication. |
| **Simulated Telemetry Input**| `DataSimulator` class running in a background `QThread`                    | Allows safe, non-blocking testing and development without relying on hardware. |
| **Live Plotting**           | Implemented using `pyqtgraph`, a high-performance plotting library         | Ensures smooth real-time updates without lag or freezing compared to heavier alternatives. |
| **Grid-Based Chart Layout** | Multiple smaller plots displayed in a grid using `QGridLayout`             | Improves readability; allows users to focus on individual parameters independently. |
| **Thread-Safe UI Updates**  | Signals emitted from background thread update UI in main thread safely     | Maintains application stability and prevents race conditions or crashes.       |
| **Data Logging and Replay** | Recorded to CSV files, with ability to replay data through custom controls | Useful for post-analysis, testing repeatability, and presentations.           |
| **Interactive Details Panel**| Shows real-time values for each parameter in a side widget                | Gives quick, digestible insights to the operator without needing to check graphs constantly. |

---

## ⚠️ Known Limitations & What We Plan to Do

| **Limitation**              | **What It Means**                                                                 | **What We Plan to Do**                                                       |
|-----------------------------|----------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| **Static X-Axis in Graphs** | Plot X-axis is currently fixed and does not scroll with incoming data                 | Implement dynamic scrolling and buffer trimming to visualize live data stream continuously |
| **Details Panel Not Updating** | Currently doesn't reflect live data changes from the simulator                      | Connect the panel to data update signals and refresh labels in real time      |
| **Only Simulated Data**     | The app uses synthetic telemetry data for now                                        | Integrate with real-time sources like serial ports, APIs, or socket streams   |
| **No User Settings Persistence** | UI choices and configurations are lost on restart                                 | Introduce config files or use `QSettings` to store user preferences           |
| **Basic Error Handling**    | Minimal checks for data format, connectivity, or empty states                        | Add exception handling and user feedback mechanisms throughout the app        |
| **Limited Map Functionality** | Map integration is stubbed but not fully implemented                                | Integrate Leaflet + GPS for real-time positional tracking in the UI           |

---
