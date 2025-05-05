# 🚀 Aerospace Control Applications

Welcome to the unified codebase for two desktop applications designed to support UAV testing and telemetry visualization:

- 🛰️ **Ground Control Station (GCS)**
- 🧪 **Thrust Stand Command Station**

Each application is modular, cross-platform, and built using **Python (PyQt5)** to provide intuitive interfaces for real-time data monitoring, plotting, and system diagnostics — whether in flight or on the test bench.

---

## 📦 Project Structure

| Application                  | Description                                                                                      | Link to Details          |
|-----------------------------|--------------------------------------------------------------------------------------------------|--------------------------|
| **Ground Control Station**  | A desktop interface to visualize UAV telemetry like GPS, battery, motor status, and attitude     | [Go to GCS UI](./ground_control_station/README.md) |
| **Thrust Stand App**        | A test bench companion app for real-time telemetry from thrust stands, motor rigs, or simulators | [Go to Thrust Stand UI](./thrust_stand_app/README.md) |

---

## 📸 UI Screenshots

### 🛰️ Ground Control Station

<!-- Replace the placeholder path with actual image file paths in your repo -->
![GCS Main UI]
*Main interface showing real-time aircraft diagnostics, map view, and telemetry widgets*
![Screenshot 2025-05-05 at 7 48 43 PM](https://github.com/user-attachments/assets/6350e691-3440-4e2b-a205-5cb243d91d09)

---

### 🧪 Thrust Stand Command Station

![Thrust Stand UI]
*Live plotting of thrust, current, RPM, and other test metrics in grid layout*
![Screenshot 2025-05-05 at 7 49 39 PM](https://github.com/user-attachments/assets/faceba7c-ed1e-4a8d-92ec-0f6271969cd5)
![image](https://github.com/user-attachments/assets/72962cb1-ec92-4f93-9a72-fdfbe3c8528a)

---

## ⚙️ How to Run

Each application is self-contained and lives in its own subdirectory. To run either:

```bash
# Step into the app directory
cd ground_control_station  # or cd thrust_stand_app

# Install dependencies
pip install -r requirements.txt

# Launch the application
python main.py
