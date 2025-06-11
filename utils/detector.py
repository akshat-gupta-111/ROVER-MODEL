import cv2
import pyttsx3
from ultralytics import YOLO
import numpy as np
import os

class BallDetector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")
        self.template_path = "ball.jpg"
        self.engine = pyttsx3.init()

    def detect_ball(self, frame, save_as_template=True, filename="ball.jpg"):
        results = self.model(frame)
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                if cls_id == 32:  # class ID 32 = sports ball
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    ball_crop = frame[y1:y2, x1:x2]
                    if ball_crop.size > 0:
                        # Resize the crop to ensure consistency
                        ball_crop = cv2.resize(ball_crop, (100, 100))
                        cv2.imwrite(filename, ball_crop)
                        if save_as_template:
                            self.template_path = filename
                            self.engine.say("Ball detected and saved.")
                        else:
                            self.engine.say("Ball captured for comparison.")
                        self.engine.runAndWait()
                        return True, (cx, cy)
        return False, None

    def compare_balls(self, file1="ball.jpg", file2="found.jpg"):
        if not os.path.exists(file1) or not os.path.exists(file2):
            print("❌ Missing template or captured ball file.")
            return False, None

        img1 = cv2.imread(file1, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(file2, cv2.IMREAD_GRAYSCALE)

        # Resize both images to standard size
        size = (100, 100)
        img1 = cv2.resize(img1, size)
        img2 = cv2.resize(img2, size)

        # Perform template matching
        res = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # Debug info
        print(f"🔍 Match confidence: {max_val:.2f}")
        threshold = 0.7

        if max_val >= threshold:
            cx = max_loc[0] + img1.shape[1] // 2
            cy = max_loc[1] + img1.shape[0] // 2
            self.engine.say("Ball matched successfully.")
            self.engine.runAndWait()
            return True, (cx, cy)
        else:
            self.engine.say("Ball did not match.")
            self.engine.runAndWait()
            return False, None