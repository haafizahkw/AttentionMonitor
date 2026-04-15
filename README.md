# AttentionMonitor

A real-time **attention monitoring system** that tracks **eye behavior, gaze direction, head movement, and awareness score** to detect distraction and drowsiness.

Built using computer vision and facial landmark tracking, the system provides **live feedback, alerts, and a dashboard UI** for monitoring user focus.

---

## Features

### Eye Tracking & Blink Detection

* Detects eye state: **Open / Closed / One Eye Closed**
* Uses Eye Aspect Ratio (EAR) for accurate detection 
* Tracks eye closure over multiple frames to avoid false positives

---

### Gaze Detection (Iris Tracking)

* Detects gaze direction:

  * Left / Right / Up / Down / Center
* Uses iris position relative to eye boundaries 
* Works only when eyes are open for better accuracy

---

### Head Movement Detection

* Tracks head orientation using facial landmarks
* Detects:

  * LEFT / RIGHT / UP / DOWN / CENTER 

---

### Awareness Scoring System

* Each subject gets a **dynamic awareness score (0–100)**
* Score decreases when:

  * Eyes are closed
  * User looks down
* Score increases when attentive
* Visualized in UI with a progress bar 

---

### Real-Time Alert System

* Triggers alert when awareness drops below threshold
* Non-blocking **beep sound using threading** 
* Prevents alert spam using control flags

---

### Multi-Person Tracking

* Supports up to **2 subjects simultaneously**
* Tracks each person independently:

  * Eye state
  * Gaze
  * Head direction
  * Awareness score

---

### Interactive Dashboard UI

* Built using **PyQt5**
* Displays:

  * Live camera feed
  * Subject cards with real-time stats
  * Awareness progress bars
  * Event log with timestamps 

---

### Event Logging System

* Logs important events:

  * Eye state changes
  * Gaze deviation
  * Head movement
* Timestamped logs for tracking behavior over time

---

## How It Works

1. Capture live video from webcam
2. Detect faces using MediaPipe Face Mesh
3. Analyze:

   * Eye aspect ratio (EAR)
   * Iris position
4.  Detect head orientation using landmarks
5.  Compute awareness score per subject
6.  Trigger alert if attention drops
7.  Display everything in real-time dashboard

---

##  Tech Stack

* **Python**
* **OpenCV**
* **MediaPipe**
* **NumPy**
* **PyQt5 (UI)**

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
│   └──facial_expression/
│       └── face_landmarks.py    # Head tracking
│   
├── ui/
│   ├── main_window.py           # Main application UI
│   ├── camera_view.py           # Camera display
│   ├── panels.py                # Info panels + logs
│   ├── dashboard.py             # Alternate dashboard
│   └── styles.py                # UI styling
│
├── config.py                    # System thresholds
├── main.py                      # Entry point
├── requirements.txt
└── README.md
```

---

##  Configuration

Modify system parameters in:

```bash
config.py
```

Includes:

* EAR threshold
* Frame threshold
* Max number of faces

---

##  Use Cases

*  Driver monitoring systems
*  Student focus tracking
*  Workplace attention monitoring
*  Human behavior analysis

---

##  Future Improvements

*  Advanced audio alerts
*  Attention analytics dashboard
*  AI-based fatigue prediction
*  Web-based deployment

---
