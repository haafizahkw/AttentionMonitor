import cv2
import mediapipe as mp
import math
import winsound
import threading

mp_face_mesh = mp.solutions.face_mesh

face_mesh_drowsy = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=2,
    refine_landmarks=True
)

threshold = 0.23

# Awareness score per face — persists across frames
awareness = {1: 100, 2: 100}

# Prevents beep from being spammed every tick
_beep_active = False


def _beep_async():
    """Play beep in background thread so it never blocks the camera."""
    global _beep_active
    _beep_active = True
    winsound.Beep(2500, 500)
    _beep_active = False


def distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)


def process_drowsiness(frame):
    """
    Analyses the frame for drowsiness per face.
    Updates awareness scores, draws overlays, beeps on low awareness.
    Returns the annotated frame and a list of dicts:
        [{"face_idx": 1, "awareness": 82}, ...]
    """
    global _beep_active

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh_drowsy.process(rgb)

    data = []

    if results.multi_face_landmarks:
        for face_id, face_landmarks in enumerate(results.multi_face_landmarks):
            idx = face_id + 1
            landmarks = face_landmarks.landmark

            # Eye landmarks
            r1, r2, r3, r4 = landmarks[33], landmarks[133], landmarks[159], landmarks[145]
            l1, l2, l3, l4 = landmarks[362], landmarks[263], landmarks[386], landmarks[374]

            # EAR
            rEAR = distance(r3, r4) / distance(r1, r2)
            lEAR = distance(l3, l4) / distance(l1, l2)
            eyes_closed = rEAR < threshold and lEAR < threshold

            # Iris vertical ratio
            iris   = landmarks[468]
            iris_y = int(iris.y * h)
            top    = int(landmarks[159].y * h)
            bottom = int(landmarks[145].y * h)
            height = bottom - top

            if height > 0:
                v_ratio = (iris_y - top) / height
            else:
                v_ratio = 0

            if v_ratio > 0.70:
                direction = "DOWN"
            elif v_ratio < 0.30:
                direction = "UP"
            else:
                direction = "CENTER"

            # Update awareness score
            if eyes_closed:
                awareness[idx] -= 2
            elif direction == "DOWN":
                awareness[idx] -= 1
            else:
                awareness[idx] += 1

            awareness[idx] = max(0, min(100, awareness[idx]))
            score = awareness[idx]

            # Overlay
            x_pos = 30 if idx == 1 else w - 280

            if score > 60:
                color = (50, 200, 50)
            elif score > 40:
                color = (0, 165, 255)
            else:
                color = (0, 0, 220)

            cv2.putText(frame,
                        f"Person {idx} Awareness: {score}%",
                        (x_pos, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            if score <= 40:
                cv2.putText(frame,
                            f"Person {idx}: LOW AWARENESS!",
                            (x_pos, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                            (0, 0, 255), 2)

                # Only start a new beep if one isn't already playing
                if not _beep_active:
                    threading.Thread(target=_beep_async, daemon=True).start()

            data.append({"face_idx": idx, "awareness": score})

    return frame, data