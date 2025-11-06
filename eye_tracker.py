# MediaPipe-based eye tracker that posts focus status to local Flask server.
import cv2, mediapipe as mp, time, requests, os
from datetime import datetime

SERVER_UPDATE_URL = 'http://127.0.0.1:5000/update'
EYE_CLOSED_THRESHOLD = 0.013  # heuristic; may need calibration per camera
LOST_FOCUS_SECONDS = 3.0

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)
cap = cv2.VideoCapture(0)

lost_start = None
currently_focused = True

print('Starting Gaze eye-tracker. Press q to quit.')

while True:
    success, frame = cap.read()
    if not success:
        print('No camera frame: check camera permissions.')
        break
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    h, w, _ = frame.shape
    display_text = 'No face detected'

    if results.multi_face_landmarks:
        lm = results.multi_face_landmarks[0].landmark
        # Using landmarks to estimate eyelid openness (approximate)
        # left eye top: 159, bottom: 145 ; right top: 386, bottom: 374 (MediaPipe indices)
        left_top = lm[159]
        left_bottom = lm[145]
        right_top = lm[386]
        right_bottom = lm[374]
        left_dist = abs(left_top.y - left_bottom.y)
        right_dist = abs(right_top.y - right_bottom.y)
        eyelid = (left_dist + right_dist) / 2.0
        display_text = f'eyelid={eyelid:.4f}'

        if eyelid < EYE_CLOSED_THRESHOLD:
            if lost_start is None:
                lost_start = time.time()
            elapsed = time.time() - lost_start
            display_text = f'Possibly distracted ({elapsed:.1f}s)'
            if elapsed >= LOST_FOCUS_SECONDS and currently_focused:
                currently_focused = False
                print('[Gaze] Focus lost:', datetime.utcnow().isoformat())
                try:
                    requests.post(SERVER_UPDATE_URL, json={'focused': False}, timeout=0.5)
                except Exception as e:
                    pass
        else:
            # eyes open; reset
            lost_start = None
            if not currently_focused:
                currently_focused = True
                print('[Gaze] Refocused:', datetime.utcnow().isoformat())
                try:
                    requests.post(SERVER_UPDATE_URL, json={'focused': True}, timeout=0.5)
                except:
                    pass
    else:
        # no face detected - treat as unfocused
        if currently_focused:
            currently_focused = False
            print('[Gaze] Face not detected - treating as unfocused')
            try:
                requests.post(SERVER_UPDATE_URL, json={'focused': False}, timeout=0.5)
            except:
                pass

    # show frame and status
    cv2.putText(frame, display_text, (20,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    cv2.imshow('Gaze - Eye Tracker (press q to quit)', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
