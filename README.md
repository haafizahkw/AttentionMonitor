# 👁️ AttentionMonitor

A real-time **attention monitoring system** that tracks **eye behavior, gaze direction, head movement, and awareness score** to detect distraction and drowsiness.

The system uses computer vision and facial landmark tracking to provide **live feedback, alerts, and an interactive dashboard UI**.

---

##  Features

###  Eye Tracking & Blink Detection

* Detects **Open / Closed / One Eye Closed**
* Uses Eye Aspect Ratio (EAR) for robust detection
* Tracks multiple frames to avoid false positives

---

###  Gaze Detection (Iris Tracking)

* Detects:

  * Left / Right / Up / Down / Center
* Uses iris position relative to eye boundaries
* Works only when eyes are open for better accuracy

---

###  Head Movement Detection

* Detects:

  * LEFT / RIGHT / UP / DOWN / CENTER
* Uses facial landmarks (MediaPipe Face Mesh)

---

###  Awareness Scoring System

* Each subject gets a **dynamic awareness score (0–100)**
* Score decreases when:

  * Eyes are closed
  * Looking down / distracted
* Score increases when attentive
* Visualized with progress bars in UI

---

###  Alert System

* Triggers alert when awareness drops below threshold
* Uses **non-blocking sound alerts**
* Prevents alert spam using control logic

---

###  Multi-Person Tracking

* Supports up to **2 subjects**
* Tracks each independently:

  * Eye state
  * Gaze direction
  * Head orientation
  * Awareness score

---

###  Interactive UI Dashboard

* Built using **PyQt5**
* Displays:

  * Live camera feed
  * Subject cards
  * Awareness bars
  * Event logs

---

###  Event Logging

* Logs:

  * Eye changes
  * Gaze movement
  * Head movement
* Timestamped for analysis

---

##  How It Works

1.  Capture live video from webcam
2.  Detect faces using MediaPipe
3.  Track eyes and iris position
4.  Estimate head orientation
5.  Compute awareness score
6.  Trigger alert if attention drops
7.  Update dashboard in real time

---

##  Tech Stack

* Python
* OpenCV
* MediaPipe
* NumPy
* PyQt5

---

##  Project Structure

```text
AttentionMonitor/

├── application/
│   └── drowsiness_detection.py   # Awareness + alert system
│
├── modules/
│   ├── eye_tracking/
│   │   └── eye.py               # Eye + gaze detection
│   │
│   └── facial_expression/
│       └── face_landmarks.py    # Head tracking
│
├── ui/
│   ├── main_window.py           # Main application UI
│   ├── camera_view.py          # Camera display
│   ├── panels.py               # Info panels + logs
│   ├── dashboard.py            # Alternate dashboard
│   └── styles.py               # UI styling
│
├── utils/
│   └── camera.py               # Camera initialization
│
├── config.py                   # System thresholds
├── main.py                     # Entry point
├── requirements.txt
└── README.md
```


---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Run the Application

```bash
python main.py
```

---

## ⚙️ Configuration

Modify system parameters in:

```bash
config.py
```

Includes:

* EAR threshold
* Frame threshold
* Max number of faces

---

## 🎯 Use Cases

* 🚗 Driver monitoring systems
* 📚 Student attention tracking
* 💻 Workplace productivity tools
* 🧠 Behavioral analysis systems

---

## 🔮 Future Improvements

* 🔊 Advanced alert system
* 📊 Analytics dashboard
* 🧠 ML-based fatigue prediction
* 🌐 Web deployment

---
