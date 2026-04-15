from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTextEdit, QProgressBar, QFrame
)
from PyQt5.QtCore import Qt
import datetime


class FaceCard(QWidget):
    def __init__(self, face_num):
        super().__init__()
        self.setObjectName("faceCard")

        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(5)
        self._layout.setContentsMargins(10, 8, 10, 10)

        # Title
        self.title = QLabel(f"── SUBJECT {face_num} ──")
        self.title.setObjectName("cardTitle")
        self._layout.addWidget(self.title)

        # Divider
        line = QFrame()
        line.setObjectName("cardDivider")
        line.setFrameShape(QFrame.HLine)
        self._layout.addWidget(line)

        # Stats
        self.eye  = QLabel("EYE  ▸  —")
        self.gaze = QLabel("GAZE ▸  —")
        self.head = QLabel("HEAD ▸  —")
        for lbl in (self.eye, self.gaze, self.head):
            lbl.setObjectName("cardStat")
            self._layout.addWidget(lbl)

        # Awareness bar row
        bar_row = QHBoxLayout()
        bar_row.setSpacing(8)

        bar_label = QLabel("AWR")
        bar_label.setObjectName("cardStat")
        bar_label.setFixedWidth(30)
        bar_row.addWidget(bar_label)

        self.awareness_bar = QProgressBar()
        self.awareness_bar.setRange(0, 100)
        self.awareness_bar.setValue(100)
        self.awareness_bar.setTextVisible(True)
        self.awareness_bar.setFormat("%v%")
        self.awareness_bar.setFixedHeight(14)
        bar_row.addWidget(self.awareness_bar)

        self._layout.addLayout(bar_row)

    def update_data(self, data):
        self.eye.setText(f"EYE  ▸  {data.get('eye_state', '—')}")
        self.gaze.setText(f"GAZE ▸  {data.get('gaze_direction', '—')}")
        self.head.setText(f"HEAD ▸  {data.get('head_direction', '—')}")

        score = data.get("awareness", 100)
        self.awareness_bar.setValue(score)
        self._set_bar_color(score)

    def reset(self):
        self.eye.setText("EYE  ▸  —")
        self.gaze.setText("GAZE ▸  —")
        self.head.setText("HEAD ▸  —")
        self.awareness_bar.setValue(100)
        self._set_bar_color(100)

    def _set_bar_color(self, score: int):
        if score > 60:
            color = "#00E5FF"   # cyan
        elif score > 40:
            color = "#FFA726"   # amber
        else:
            color = "#EF5350"   # red
        self.awareness_bar.setStyleSheet(
            f"QProgressBar::chunk {{ background-color: {color}; border-radius: 2px; }}"
        )


class InfoPanels(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(10)
        self._layout.setContentsMargins(4, 0, 0, 0)

        # Face cards
        self.face_cards = []
        for i in range(1, 3):
            card = FaceCard(i)
            self.face_cards.append(card)
            self._layout.addWidget(card)

        self._layout.addStretch()

        # Log title
        log_title = QLabel("── EVENT LOG ──")
        log_title.setObjectName("cardTitle")
        self._layout.addWidget(log_title)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setFixedHeight(160)
        self._layout.addWidget(self.log_area)

        self._log_lines = []

    def update_faces(self, face_data_list):
        active_indices = set()

        for data in face_data_list:
            idx = data["face_idx"] - 1

            if idx < len(self.face_cards):
                eye_raw = data.get("eye_state", "—")
                eye_state = "CLOSED" if "Closed" in eye_raw else "OPEN"

                adapted_data = {
                    "eye_state":      eye_state,
                    "gaze_direction": data.get("gaze_direction", "—").upper(),
                    "head_direction": data.get("head_direction", "—").upper(),
                    "awareness":      data.get("awareness", 100),
                }

                self.face_cards[idx].update_data(adapted_data)
                active_indices.add(idx)

        for i, fc in enumerate(self.face_cards):
            if i not in active_indices:
                fc.reset()

    def append_log(self, message: str):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self._log_lines.append(f"[{ts}]  {message.upper()}")

        if len(self._log_lines) > 100:
            self._log_lines.pop(0)

        self.log_area.setPlainText("\n".join(reversed(self._log_lines)))