import cv2
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QFrame
)
from PyQt5.QtCore import QTimer, Qt, QDateTime

from ui.camera_view import CameraView
from ui.panels import InfoPanels
from ui.styles import STYLESHEET

from modules.eye_tracking.eye import process_frame
from modules.facial_expression.face_landmarks import process_head
from application.drowsiness_detection import process_drowsiness
from utils.camera import get_camera

TIMER_MS = 30


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("EYE TRACKING SYSTEM")
        self.setMinimumSize(1200, 720)
        self.setStyleSheet(STYLESHEET)

        self.cap = get_camera()
        self._prev_states = {}

        # ===== UI SETUP =====
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(16, 14, 16, 10)
        root.setSpacing(10)

        # ── Header ──────────────────────────────────────────
        header = QWidget()
        hl = QHBoxLayout(header)
        hl.setContentsMargins(0, 0, 0, 0)

        # Left: system title
        title = QLabel("👁  EYE TRACKING SYSTEM")
        title.setObjectName("titleLabel")

        # Center: live clock
        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignCenter)
        self.clock_label.setStyleSheet("""
            font-size: 11px;
            color: #2A6F8A;
            letter-spacing: 3px;
        """)

        # Right: subtitle
        subtitle = QLabel("REAL-TIME MONITOR  v1.0")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        hl.addWidget(title)
        hl.addStretch()
        hl.addWidget(self.clock_label)
        hl.addStretch()
        hl.addWidget(subtitle)

        root.addWidget(header)

        # ── Divider ──────────────────────────────────────────
        div = QFrame()
        div.setObjectName("divider")
        div.setFrameShape(QFrame.HLine)
        root.addWidget(div)

        # ── Body ─────────────────────────────────────────────
        body = QHBoxLayout()
        body.setSpacing(12)

        self.camera_view = CameraView()
        body.addWidget(self.camera_view, 3)

        self.panels = InfoPanels()
        self.panels.setFixedWidth(280)
        body.addWidget(self.panels, 1)

        root.addLayout(body)

        # ── Status bar ───────────────────────────────────────
        status_div = QFrame()
        status_div.setObjectName("divider")
        status_div.setFrameShape(QFrame.HLine)
        root.addWidget(status_div)

        self.status_label = QLabel("◉  SYSTEM ONLINE  ·  CAMERA ACTIVE  ·  TRACKING 0 SUBJECTS")
        self.status_label.setStyleSheet("""
            font-size: 9px;
            color: #2A6F8A;
            letter-spacing: 2px;
            padding: 2px 0px;
        """)
        root.addWidget(self.status_label)

        # ── Timers ───────────────────────────────────────────
        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)
        self.timer.start(TIMER_MS)

        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self._update_clock)
        self.clock_timer.start(1000)
        self._update_clock()

    # ===== CLOCK =====
    def _update_clock(self):
        now = QDateTime.currentDateTime().toString("yyyy-MM-dd  HH:mm:ss")
        self.clock_label.setText(now)

    # ===== MAIN LOOP =====
    def _tick(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)

        # Eye tracking
        annotated_frame, face_data_list = process_frame(frame)

        # Head tracking
        head_data_list = process_head(frame)

        # Drowsiness
        annotated_frame, drowsy_data_list = process_drowsiness(annotated_frame)

        # Merge head direction
        for face in face_data_list:
            face["head_direction"] = "N/A"
            for head in head_data_list:
                if face["face_idx"] == head["face_idx"]:
                    face["head_direction"] = head["head"]
                    break

        # Merge awareness score
        for face in face_data_list:
            face["awareness"] = 100
            for drowsy in drowsy_data_list:
                if face["face_idx"] == drowsy["face_idx"]:
                    face["awareness"] = drowsy["awareness"]
                    break

        # Update status bar
        count = len(face_data_list)
        self.status_label.setText(
            f"◉  SYSTEM ONLINE  ·  CAMERA ACTIVE  ·  TRACKING {count} SUBJECT{'S' if count != 1 else ''}"
        )

        # UI updates
        self.camera_view.update_frame(annotated_frame)
        self.panels.update_faces(face_data_list)
        self._log_changes(face_data_list)

    # ===== LOG SYSTEM =====
    def _log_changes(self, face_data_list):
        for data in face_data_list:
            idx   = data["face_idx"]
            state = data["eye_state"]
            gaze  = data["gaze_direction"]
            head  = data.get("head_direction", "N/A")

            prev = self._prev_states.get(idx, (None, None, None))

            if state != prev[0]:
                self.panels.append_log(f"Subject {idx} eye → {state}")

            if gaze != prev[1] and gaze != "Looking Center":
                self.panels.append_log(f"Subject {idx} gaze → {gaze}")

            if head != prev[2] and head != "CENTER":
                self.panels.append_log(f"Subject {idx} head → {head}")

            self._prev_states[idx] = (state, gaze, head)

    def closeEvent(self, event):
        self.timer.stop()
        self.clock_timer.stop()
        self.cap.release()
        super().closeEvent(event)