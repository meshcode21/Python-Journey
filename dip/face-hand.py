"""
🖐️ Hand Gesture & Face Tracker
================================
Uses OpenCV + MediaPipe to track:
  - Both hands with individual finger states
  - Face mesh with key landmarks
  - Gesture recognition (peace ✌️, thumbs up 👍, fist ✊, open hand 🖐️, point ☝️)
  - Finger count display
  - FPS counter

Controls:
  Q  → Quit
  F  → Toggle face mesh
  H  → Toggle hand tracking
  L  → Toggle landmark labels
  S  → Save screenshot
"""

import cv2
import mediapipe as mp
import numpy as np
import time
import os

# ──────────────────────────────────────────────────────────
# Setup MediaPipe
# ──────────────────────────────────────────────────────────
mp_hands   = mp.solutions.hands
mp_face    = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

FINGER_TIPS   = [4, 8, 12, 16, 20]          # thumb, index, middle, ring, pinky
FINGER_NAMES  = ["Thumb", "Index", "Middle", "Ring", "Pinky"]

# ──────────────────────────────────────────────────────────
# Gesture Recognition
# ──────────────────────────────────────────────────────────
def get_finger_states(hand_landmarks, handedness):
    """Return list of booleans: True = finger is up/extended."""
    lm = hand_landmarks.landmark
    states = []

    # Thumb – compare tip x vs IP joint (mirror for left hand)
    if handedness == "Right":
        states.append(lm[4].x < lm[3].x)
    else:
        states.append(lm[4].x > lm[3].x)

    # Other four fingers – tip y above PIP joint
    for tip in FINGER_TIPS[1:]:
        states.append(lm[tip].y < lm[tip - 2].y)

    return states   # [thumb, index, middle, ring, pinky]


def classify_gesture(states):
    thumb, index, middle, ring, pinky = states
    count = sum(states)

    if count == 0:
        return "✊ Fist", (0, 0, 200)
    if count == 5:
        return "🖐 Open Hand", (0, 200, 100)
    if index and middle and not ring and not pinky and not thumb:
        return "✌️ Peace", (200, 150, 0)
    if index and not middle and not ring and not pinky:
        return "☝️ Point", (150, 0, 200)
    if thumb and not index and not middle and not ring and not pinky:
        return "👍 Thumbs Up", (0, 180, 255)
    if thumb and pinky and not index and not middle and not ring:
        return "🤙 Call Me", (255, 100, 0)
    if index and middle and ring and pinky and not thumb:
        return "Four Fingers", (100, 200, 200)
    return f"{count} Fingers", (180, 180, 180)

# ──────────────────────────────────────────────────────────
# Drawing Helpers
# ──────────────────────────────────────────────────────────
HAND_COLORS = {
    "Right": (0, 220, 150),   # teal-green
    "Left":  (255, 140, 0),   # orange
}

def draw_rounded_rect(img, x1, y1, x2, y2, color, radius=12, alpha=0.55):
    overlay = img.copy()
    cv2.rectangle(overlay, (x1 + radius, y1), (x2 - radius, y2), color, -1)
    cv2.rectangle(overlay, (x1, y1 + radius), (x2, y2 - radius), color, -1)
    for cx, cy in [(x1+radius, y1+radius), (x2-radius, y1+radius),
                   (x1+radius, y2-radius), (x2-radius, y2-radius)]:
        cv2.circle(overlay, (cx, cy), radius, color, -1)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)


def draw_finger_dots(frame, hand_landmarks, h, w, states, color):
    for i, tip_id in enumerate(FINGER_TIPS):
        lm = hand_landmarks.landmark[tip_id]
        cx, cy = int(lm.x * w), int(lm.y * h)
        dot_color = (0, 255, 100) if states[i] else (0, 60, 200)
        cv2.circle(frame, (cx, cy), 14, dot_color, -1)
        cv2.circle(frame, (cx, cy), 14, (255, 255, 255), 2)
        cv2.putText(frame, FINGER_NAMES[i][0], (cx - 5, cy + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)


def put_label(frame, text, pos, font_scale=0.65, color=(255,255,255), thickness=1):
    cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_DUPLEX,
                font_scale, (0, 0, 0), thickness + 2)
    cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_DUPLEX,
                font_scale, color, thickness)

# ──────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────
def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot open camera. Check your webcam connection.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    show_face   = True
    show_hands  = True
    show_labels = True
    screenshot_count = 0

    prev_time = time.time()

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6,
    )
    face_mesh = mp_face.FaceMesh(
        static_image_mode=False,
        max_num_faces=2,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    print("🎥 Tracker running! Controls:  Q=quit  F=face  H=hands  L=labels  S=screenshot")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️  Failed to grab frame.")
            break

        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]
        rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # ── Face Mesh ─────────────────────────────────────
        if show_face:
            face_results = face_mesh.process(rgb)
            if face_results.multi_face_landmarks:
                for face_lms in face_results.multi_face_landmarks:
                    # Draw tesselation (subtle)
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_lms,
                        connections=mp_face.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                            .get_default_face_mesh_tesselation_style(),
                    )
                    # Draw contours
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_lms,
                        connections=mp_face.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                            .get_default_face_mesh_contours_style(),
                    )
                    # Eye irises
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_lms,
                        connections=mp_face.FACEMESH_IRISES,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                            .get_default_face_mesh_iris_connections_style(),
                    )

        # ── Hands ─────────────────────────────────────────
        gesture_texts = []
        if show_hands:
            hand_results = hands.process(rgb)
            if hand_results.multi_hand_landmarks:
                for hand_lms, hand_info in zip(
                    hand_results.multi_hand_landmarks,
                    hand_results.multi_handedness
                ):
                    label = hand_info.classification[0].label   # "Left" / "Right"
                    color = HAND_COLORS[label]

                    # Draw skeleton
                    mp_drawing.draw_landmarks(
                        frame, hand_lms, mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style(),
                    )

                    states = get_finger_states(hand_lms, label)
                    gesture, g_color = classify_gesture(states)
                    gesture_texts.append((label, gesture, g_color, states))

                    draw_finger_dots(frame, hand_lms, h, w, states, color)

                    # Wrist label
                    wrist = hand_lms.landmark[0]
                    wx, wy = int(wrist.x * w), int(wrist.y * h)
                    if show_labels:
                        put_label(frame, f"{label} Hand", (wx - 40, wy + 30),
                                  color=color, font_scale=0.55)

        # ── HUD Panel (top-left) ───────────────────────────
        panel_h = 42 + len(gesture_texts) * 36
        draw_rounded_rect(frame, 10, 10, 340, panel_h, (20, 20, 30))

        # FPS
        now  = time.time()
        fps  = 1 / max(now - prev_time, 1e-6)
        prev_time = now
        put_label(frame, f"FPS: {fps:.1f}", (22, 36), font_scale=0.7,
                  color=(100, 255, 180), thickness=1)

        for i, (side, gesture, g_color, states) in enumerate(gesture_texts):
            y = 68 + i * 36
            finger_count = sum(states)
            put_label(frame, f"{side}: {gesture}  [{finger_count}]",
                      (22, y), font_scale=0.62, color=g_color)

        # ── Key Legend (bottom) ────────────────────────────
        legend = "Q:Quit  F:Face  H:Hands  L:Labels  S:Screenshot"
        draw_rounded_rect(frame, 10, h - 38, len(legend) * 9 + 20, h - 8,
                          (20, 20, 30))
        put_label(frame, legend, (18, h - 18), font_scale=0.48,
                  color=(200, 200, 200))

        # ── Toggle indicators ──────────────────────────────
        indicators = [
            ("FACE",  show_face,  (w - 260, 32)),
            ("HANDS", show_hands, (w - 170, 32)),
            ("LABELS",show_labels,(w -  70, 32)),
        ]
        draw_rounded_rect(frame, w - 275, 10, w - 10, 48, (20, 20, 30))
        for name, active, pos in indicators:
            col = (0, 230, 120) if active else (80, 80, 80)
            put_label(frame, name, pos, font_scale=0.45, color=col)

        cv2.imshow("🖐 Hand & Face Tracker — Press Q to quit", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('f'):
            show_face = not show_face
            print(f"Face mesh: {'ON' if show_face else 'OFF'}")
        elif key == ord('h'):
            show_hands = not show_hands
            print(f"Hand tracking: {'ON' if show_hands else 'OFF'}")
        elif key == ord('l'):
            show_labels = not show_labels
        elif key == ord('s'):
            fname = f"screenshot_{screenshot_count:03d}.png"
            cv2.imwrite(fname, frame)
            screenshot_count += 1
            print(f"📸 Saved {fname}")

    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    face_mesh.close()
    print("👋 Tracker closed.")


if __name__ == "__main__":
    main()