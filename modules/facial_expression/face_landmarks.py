# import cv2
# import mediapipe as mp

# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# mp_face_mesh = mp.solutions.face_mesh

# cap = cv2.VideoCapture(0)

# with mp_face_mesh.FaceMesh(
#     max_num_faces=1,
#     refine_landmarks=True,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5
# ) as face_mesh:

#     while cap.isOpened():
#         success, image = cap.read()
#         if not success:
#             break

#         image = cv2.flip(image, 1)  # fix mirror issue

#         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         results = face_mesh.process(image_rgb)

#         direction = "No Face"

#         if results.multi_face_landmarks:
#             for face_landmarks in results.multi_face_landmarks:

#                 h, w, _ = image.shape

#                 # Important landmarks
#                 nose = face_landmarks.landmark[1]
#                 left_eye = face_landmarks.landmark[33]
#                 right_eye = face_landmarks.landmark[263]
#                 chin = face_landmarks.landmark[152]
#                 forehead = face_landmarks.landmark[10]

#                 # Convert to pixel
#                 nose_x = int(nose.x * w)
#                 nose_y = int(nose.y * h)

#                 left_x = int(left_eye.x * w)
#                 right_x = int(right_eye.x * w)

#                 chin_y = int(chin.y * h)
#                 forehead_y = int(forehead.y * h)

#                 # Horizontal movement
#                 left_dist = abs(nose_x - left_x)
#                 right_dist = abs(nose_x - right_x)

#                 if left_dist < right_dist - 10:
#                     horiz = "LEFT"
#                 elif right_dist < left_dist - 10:
#                     horiz = "RIGHT"
#                 else:
#                     horiz = "CENTER"

#                 # Vertical movement
#                 face_height = chin_y - forehead_y
#                 mid_y = forehead_y + face_height // 2

#                 if nose_y < mid_y - 10:
#                     vert = "UP"
#                 elif nose_y > mid_y + 10:
#                     vert = "DOWN"
#                 else:
#                     vert = "CENTER"

#                 # Combine
#                 if horiz == "CENTER" and vert == "CENTER":
#                     direction = "CENTER"
#                 elif horiz == "CENTER":
#                     direction = f"CENTER-{vert}"
#                 elif vert == "CENTER":
#                     direction = f"{horiz}"
#                 else:
#                     direction = f"{horiz}-{vert}"

#                 # Draw landmarks
#                 mp_drawing.draw_landmarks(
#                     image=image,
#                     landmark_list=face_landmarks,
#                     connections=mp_face_mesh.FACEMESH_TESSELATION,
#                     landmark_drawing_spec=None,
#                     connection_drawing_spec=
#                     mp_drawing_styles.get_default_face_mesh_tesselation_style()
#                 )

#         # Show direction
#         cv2.putText(image, direction, (30, 50),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1,
#                     (0, 255, 0), 2)

#         cv2.imshow("Face Movement Detection", image)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# cap.release()
# cv2.destroyAllWindows()


import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

face_mesh_head = mp_face_mesh.FaceMesh(
    max_num_faces=2,
    refine_landmarks=True
)

def process_head(frame):

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh_head.process(rgb)

    heads = []

    if results.multi_face_landmarks:
        for face_id, face_landmarks in enumerate(results.multi_face_landmarks):

            landmarks = face_landmarks.landmark

            nose = landmarks[1]
            left_eye = landmarks[33]
            right_eye = landmarks[263]
            chin = landmarks[152]
            forehead = landmarks[10]

            nose_x = int(nose.x * w)
            nose_y = int(nose.y * h)

            left_x = int(left_eye.x * w)
            right_x = int(right_eye.x * w)

            chin_y = int(chin.y * h)
            forehead_y = int(forehead.y * h)

            # Horizontal
            left_dist = abs(nose_x - left_x)
            right_dist = abs(nose_x - right_x)

            if left_dist < right_dist - 10:
                horiz = "LEFT"
            elif right_dist < left_dist - 10:
                horiz = "RIGHT"
            else:
                horiz = "CENTER"

            # Vertical
            face_height = chin_y - forehead_y
            mid_y = forehead_y + face_height // 2
            threshold_y = face_height * 0.08

            if nose_y < mid_y - threshold_y:
                vert = "UP"
            elif nose_y > mid_y + threshold_y:
                vert = "DOWN"
            else:
                vert = "CENTER"

            if horiz == "CENTER" and vert == "CENTER":
                head = "CENTER"
            elif horiz == "CENTER":
                head = f"CENTER-{vert}"
            elif vert == "CENTER":
                head = horiz
            else:
                head = f"{horiz}-{vert}"

            heads.append({
                "face_idx": face_id + 1,
                "head": head
            })

    return heads