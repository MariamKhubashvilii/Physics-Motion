import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def process(self, frame):
        # MediaPipe needs RGB, OpenCV gives BGR
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)
        return self.results

    def get_landmarks(self, frame_shape):
        """Returns list of 21 (x, y, z) points per hand, in pixel coords"""
        h, w = frame_shape[:2]
        all_hands = []
        if self.results and self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                points = []
                for lm in hand_landmarks.landmark:
                    # lm.x and lm.y are 0-1 normalized, z is depth
                    points.append((int(lm.x * w), int(lm.y * h), lm.z))
                all_hands.append(points)
        return all_hands

    def draw_landmarks(self, frame):
        if self.results and self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        return frame