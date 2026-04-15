from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QWidget,
    QHBoxLayout, QVBoxLayout
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import cv2
import mediapipe as mp
import math


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Eye Tracking Dashboard")
        self.setGeometry(100, 100, 1100, 600)

        # UI Layout
        self.video_label = QLabel()
        self.info_layout = QVBoxLayout()

        right_widget = QWidget()
        right_widget.setLayout(self.info_layout)

        layout = QHBoxLayout()
        layout.addWidget(self.video_label, 3)
        layout.addWidget(right_widget, 1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Camera
        self.cap = cv2.VideoCapture(0)

        # Mediapipe setup (same as your code)
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=2,
            refine_landmarks=True
        )

        self.left_closed_frames = [0, 0]
        self.right_closed_frames = [0, 0]

        self.RIGHT_IRIS = [469,470,471,472]
        self.LEFT_IRIS = [474,475,476,477]

        self.threshold = 0.23
        self.min_frames = 5

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def distance(self, p1, p2):
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        data = []

        if results.multi_face_landmarks:
            for face_id, face_landmarks in enumerate(results.multi_face_landmarks):

                landmarks = face_landmarks.landmark

                # === SAME LOGIC (UNCHANGED) ===
                r1, r2, r3, r4 = landmarks[33], landmarks[133], landmarks[159], landmarks[145]
                l1, l2, l3, l4 = landmarks[362], landmarks[263], landmarks[386], landmarks[374]

                r_ear = self.distance(r3, r4) / self.distance(r1, r2)
                l_ear = self.distance(l3, l4) / self.distance(l1, l2)

                gaze = "N/A"

                if r_ear > self.threshold and l_ear > self.threshold:
                    iris_rx = int(landmarks[468].x * w)
                    iris_lx = int(landmarks[473].x * w)

                    rlx, rrx = int(landmarks[33].x * w), int(landmarks[133].x * w)
                    llx, lrx = int(landmarks[362].x * w), int(landmarks[263].x * w)

                    gaze_ratio = ((iris_rx - rlx) / (rrx - rlx) +
                                  (iris_lx - llx) / (lrx - llx)) / 2

                    if gaze_ratio < 0.35:
                        gaze = "Right"
                    elif gaze_ratio > 0.65:
                        gaze = "Left"
                    else:
                        gaze = "Center"

                # Eye state
                if l_ear < self.threshold:
                    self.left_closed_frames[face_id] += 1
                else:
                    self.left_closed_frames[face_id] = 0

                if r_ear < self.threshold:
                    self.right_closed_frames[face_id] += 1
                else:
                    self.right_closed_frames[face_id] = 0

                if self.left_closed_frames[face_id] >= self.min_frames and self.right_closed_frames[face_id] >= self.min_frames:
                    eye = "Closed"
                elif self.left_closed_frames[face_id] >= self.min_frames or self.right_closed_frames[face_id] >= self.min_frames:
                    eye = "One Eye Closed"
                else:
                    eye = "Open"

                data.append({
                    "person": face_id + 1,
                    "eye": eye,
                    "gaze": gaze
                })

        # Show camera
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qt_img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_img))

        # Update dashboard
        for i in reversed(range(self.info_layout.count())):
            widget = self.info_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for person in data:
            label = QLabel(f"""
            <b>Person {person['person']}</b><br>
            Eye: {person['eye']}<br>
            Gaze: {person['gaze']}
            """)

            label.setStyleSheet("""
                background:#1e1e1e;
                color:white;
                padding:10px;
                border-radius:8px;
            """)

            self.info_layout.addWidget(label)

    def closeEvent(self, event):
        self.cap.release()