import cv2
import time
import numpy as np
from hand_tracker import HandTracker
from gestures import get_gesture
from physics_engine import PhysicsEngine
from renderer import Renderer

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    tracker  = HandTracker()
    engine   = PhysicsEngine(W, H)
    renderer = Renderer(W, H)

    grabbed_obj = None        # object currently being dragged
    prev_hand_pos = None      # for calculating throw velocity
    prev_time = time.time()
    last_gesture = "none"
    gesture_cooldown = 0      # frames to wait before re-triggering

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)   # mirror so it feels natural
        dt = min(time.time() - prev_time, 0.05)   # cap dt to avoid explosions
        prev_time = time.time()

        # --- Hand tracking ---
        tracker.process(frame)
        all_hands = tracker.get_landmarks(frame.shape)
        tracker.draw_landmarks(frame)

        gesture = "none"
        hand_pos = None

        if all_hands:
            landmarks = all_hands[0]
            gesture = get_gesture(landmarks)
            # Use index fingertip (landmark 8) as main interaction point
            hand_pos = landmarks[8]   # (x, y, z)

        # --- Gesture logic ---
        if gesture_cooldown > 0:
            gesture_cooldown -= 1

        if hand_pos and gesture_cooldown == 0:
            hx, hy, hz = hand_pos

            if gesture == "pinch":
                engine.spawn(hx, hy, hz * -300)   # z scaled to depth range
                gesture_cooldown = 20

            elif gesture == "fist":
                engine.delete_nearest(hx, hy)
                gesture_cooldown = 20

            elif gesture == "open_palm":
                engine.paused = not engine.paused
                gesture_cooldown = 30

            elif gesture == "peace" and last_gesture != "peace":
                engine.toggle_mode()
                gesture_cooldown = 30

            elif gesture == "point":
                # Find closest object to fingertip and grab it
                if grabbed_obj is None:
                    for obj in engine.objects:
                        dist = ((obj.pos[0]-hx)**2 + (obj.pos[1]-hy)**2)**0.5
                        if dist < obj.radius * 2.5:
                            grabbed_obj = obj
                            break
                if grabbed_obj:
                    # Calculate velocity from hand movement for throwing
                    if prev_hand_pos:
                        px, py, pz = prev_hand_pos
                        throw_vel = np.array([
                            (hx - px) / dt,
                            (hy - py) / dt,
                            0.0
                        ])
                    grabbed_obj.pos[0] = hx
                    grabbed_obj.pos[1] = hy
                    grabbed_obj.vel = np.array([0.0, 0.0, 0.0])

            if gesture != "point" and grabbed_obj:
                # Release -- apply throw velocity
                if prev_hand_pos:
                    px, py, _ = prev_hand_pos
                    grabbed_obj.vel = np.array([
                        (hx - px) / dt * 0.8,
                        (hy - py) / dt * 0.8,
                        0.0
                    ])
                grabbed_obj = None

            prev_hand_pos = hand_pos

        last_gesture = gesture

        # --- Physics update ---
        engine.update(dt)

        # --- Render ---
        renderer.draw_objects(frame, engine.objects, engine.mode)
        renderer.draw_hud(frame, engine.mode, engine.paused, gesture)

        cv2.imshow("Physics Sim", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()