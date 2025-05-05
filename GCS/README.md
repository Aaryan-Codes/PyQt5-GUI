# Ground Control Station (GCS) – 📘 Overview

The Ground Control Station (GCS) is a modular desktop application built using **PyQt5**, designed to provide a real-time interface for monitoring UAV telemetry and sensor data. It simulates a working ground station setup with key visual elements such as aircraft attitude, GPS status, battery performance, and motor diagnostics — all delivered through intuitive UI widgets.

Currently, the app uses **simulated (dummy) data** to help us prototype and validate the interface and system behavior without requiring a live UAV feed.

---

## 🧠 Design Decisions & Rationale

We followed a modular design philosophy, similar to what is commonly seen in aviation tools like QGroundControl. Here’s a quick look at the key design choices and why they made sense:

| **Design Decision**          | **Chosen Approach**                                   | **Rationale**                                                                 |
|--------------------------|--------------------------------------------------|----------------------------------------------------------------------------------|
| **UI Framework**         | PyQt5                                            | Offers a powerful, flexible GUI toolkit with support for widgets, threading, and web views |
| **Architecture**         | Component-based (each widget is self-contained)  | Makes the app easier to maintain, extend, and debug                             |
| **Data Handling**        | Background thread with mock data generator       | Prevents UI from freezing while simulating real-time telemetry                  |
| **Map Integration**      | Leaflet via QWebEngineView                       | Provides an interactive map without relying on expensive GIS toolkits           |
| **UI Updates**           | Signals and timers                               | Ensures smooth communication between threads and responsive updates             |

This setup also mirrors real-world architecture, which means swapping out the mock data for real-time telemetry later on will be straightforward.

---

## ⚠️ Known Limitations and What We Plan to Do

While the app works well for simulation, we’re aware of a few areas where there’s room for improvement:

| **Limitation**                            | **What It Means**                                                                       | **What We Plan To Do**                                                  |
|-------------------------------------------|------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| **No real telemetry yet**                 | Currently powered by a data simulator                                                   | Integrate MAVSDK/MAVLink for live data from drones                     |
| **Basic visual style**                    | Lacks advanced themes or a modern design touch                                          | Apply Qt Style Sheets (QSS) or use libraries like `QDarkStyle`         |
| **Performance scaling**                   | UI responsiveness could drop at higher update frequencies                              | Optimize with throttling or switch to `pyqtgraph` for heavy plotting   |
| **Fixed layout and sizing**               | Limited responsiveness across different screen sizes                                   | Enhance layout flexibility and add resolution scaling features         |

---
