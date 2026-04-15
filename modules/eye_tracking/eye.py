import cv2
import mediapipe as mp
import math

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=2,
    refine_landmarks=True
)


left_closed_frames = [0,0]
right_closed_frames = [0,0]

RIGHT_IRIS = [469,470,471,472]
LEFT_IRIS = [474,475,476,477]

threshold = 0.23
min_frames = 5

def distance(p1,p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def process_frame(frame):

    h, w, _ = frame.shape
    data = [] 
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)
    

    if results.multi_face_landmarks:

        for face_id, face_landmarks in enumerate(results.multi_face_landmarks):
            gaze = "N/A"

            landmarks = face_landmarks.landmark

            # RIGHT EYE LANDMARKS
            r1 = landmarks[33]
            r2 = landmarks[133]
            r3 = landmarks[159]
            r4 = landmarks[145]

            # LEFT EYE LANDMARKS
            l1 = landmarks[362]
            l2 = landmarks[263]
            l3 = landmarks[386]
            l4 = landmarks[374]


            # RIGHT IRIS CENTER
            iris_r = landmarks[468]

            iris_rx = int(iris_r.x * w)
            iris_ry = int(iris_r.y * h)


            # LEFT IRIS CENTER
            iris_l = landmarks[473]

            iris_lx = int(iris_l.x * w)
            iris_ly = int(iris_l.y * h)


            # Convert to pixel coordinates
            r1p = (int(r1.x*w), int(r1.y*h))
            r2p = (int(r2.x*w), int(r2.y*h))
            r3p = (int(r3.x*w), int(r3.y*h))
            r4p = (int(r4.x*w), int(r4.y*h))

            l1p = (int(l1.x*w), int(l1.y*h))
            l2p = (int(l2.x*w), int(l2.y*h)) 
            l3p = (int(l3.x*w), int(l3.y*h))
            l4p = (int(l4.x*w), int(l4.y*h))


            # Draw eye mesh (only around eyes)
           # cv2.line(frame,r1p,r3p,(0,255,0),1)
           # cv2.line(frame,r3p,r2p,(0,255,0),1)
            #cv2.line(frame,r2p,r4p,(0,255,0),1)
            #cv2.line(frame,r4p,r1p,(0,255,0),1)

            #cv2.line(frame,l1p,l3p,(0,255,0),1)
           # cv2.line(frame,l3p,l2p,(0,255,0),1)
            #cv2.line(frame,l2p,l4p,(0,255,0),1)
            #cv2.line(frame,l4p,l1p,(0,255,0),1)


            # EAR for right eye
            r_horizontal = distance(r1,r2)
            r_vertical = distance(r3,r4)
            r_ear = r_vertical / r_horizontal


            # EAR for left eye
            l_horizontal = distance(l1,l2)
            l_vertical = distance(l3,l4)
            l_ear = l_vertical / l_horizontal
            
            # Detect gaze only if both eyes are open
            if r_ear > threshold and l_ear > threshold:

                iris_r = landmarks[468]
                iris_l = landmarks[473]

                iris_rx = int(iris_r.x * w)
                iris_lx = int(iris_l.x * w)

                rlx = int(landmarks[33].x * w)
                rrx = int(landmarks[133].x * w)

                llx = int(landmarks[362].x * w)
                lrx = int(landmarks[263].x * w)

                ratio_r = (iris_rx - rlx) / (rrx - rlx)
                ratio_l = (iris_lx - llx) / (lrx - llx)

                gaze_ratio = (ratio_r + ratio_l) / 2

                # iris vertical positions
                iris_ry = int(landmarks[468].y * h)
                iris_ly = int(landmarks[473].y * h)

                # eyelids
                top_r = int(landmarks[159].y * h)
                bottom_r = int(landmarks[145].y * h)

                top_l = int(landmarks[386].y * h)
                bottom_l = int(landmarks[374].y * h)

                ratio_updown_r = (iris_ry - top_r) / (bottom_r - top_r)
                ratio_updown_l = (iris_ly - top_l) / (bottom_l - top_l)

                vertical_ratio = (ratio_updown_r + ratio_updown_l) / 2

                # horizontal direction
                if gaze_ratio < 0.35:
                    gaze = "Looking Right"

                elif gaze_ratio > 0.65:
                    gaze = "Looking Left"

                # vertical direction
                elif vertical_ratio < 0.35:
                    gaze = "Looking Up"

                elif vertical_ratio > 0.65:
                    gaze = "Looking Down"

                else:
                    gaze = "Looking Center"

                if face_id == 0:
                    gaze_x = 30
                    label = "Person 1"
                else:
                    gaze_x = w - 300
                    label = "Person 2"

                cv2.putText(frame, f"{label}: {gaze}",
                            (gaze_x, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)
                

            #When right eye is open, draw iris landmarks
            if r_ear > threshold:   
                for idx in RIGHT_IRIS:
                    x = int(landmarks[idx].x * w)
                    y = int(landmarks[idx].y * h)
                    cv2.circle(frame, (x, y), 2, (255,255,255), -1)
            

            #When left eye is open, draw iris landmarks
            if l_ear > threshold:   
                for idx in LEFT_IRIS:
                    x = int(landmarks[idx].x * w)
                    y = int(landmarks[idx].y * h)
                    cv2.circle(frame, (x, y), 2, (255,255,255), -1)


            # Eye condition logic
            # LEFT EYE
            if l_ear < threshold:
                left_closed_frames[face_id] += 1
            else:
                left_closed_frames[face_id] = 0

            # RIGHT EYE
            if r_ear < threshold:
                right_closed_frames[face_id] += 1
            else:
                right_closed_frames[face_id] = 0


            if left_closed_frames[face_id] >= min_frames and right_closed_frames[face_id] >= min_frames:
                text = "Eyes Closed"
                color = (0, 0, 255)
                cv2.line(frame,r1p,r3p,(0, 0, 255),1)
                cv2.line(frame,r3p,r2p,(0, 0, 255),1)
                cv2.line(frame,r2p,r4p,(0, 0, 255),1)
                cv2.line(frame,r4p,r1p,(0, 0, 255),1)

                cv2.line(frame,l1p,l3p,(0, 0, 255),1)
                cv2.line(frame,l3p,l2p,(0, 0, 255),1)
                cv2.line(frame,l2p,l4p,(0, 0, 255),1)
                cv2.line(frame,l4p,l1p,(0, 0, 255),1)

            elif left_closed_frames[face_id] >= min_frames:
                text = "One Eye Closed"
                color = (0, 255, 255)
                cv2.line(frame,l1p,l3p,(0, 255, 255),1)
                cv2.line(frame,l3p,l2p,(0, 255, 255),1)
                cv2.line(frame,l2p,l4p,(0, 255, 255),1)
                cv2.line(frame,l4p,l1p,(0, 255, 255),1)
            
            elif right_closed_frames[face_id] >= min_frames:
                text = "One Eye Closed"
                color = (0, 255, 255)
                cv2.line(frame,r1p,r3p,(0, 255, 255),1)
                cv2.line(frame,r3p,r2p,(0, 255, 255),1)
                cv2.line(frame,r2p,r4p,(0, 255, 255),1)
                cv2.line(frame,r4p,r1p,(0, 255, 255),1)
            else:
                text = "Eyes Open"
                color = (0, 255, 0)

            #y_position = 40 + face_id*40

            #cv2.putText(frame, text, (30, y_position),
                        #cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            y_offset = 40

            if face_id == 0:
                x_position = 30
                label = "Person 1"
            else:
                x_position = w - 300
                label = "Person 2"

            cv2.putText(frame, f"{label}: {text}",
                        (x_position, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)        

            data.append({
              "face_idx": face_id + 1,
              "eye_state": text,
              "gaze_direction": gaze
              })

    return frame, data
  
   

