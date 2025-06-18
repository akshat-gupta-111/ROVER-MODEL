import cv2
from utils.detector import BallDetector
from utils.voice_listener import listen_for_command

def main():
    
    detector = BallDetector()

    while True:
        command = listen_for_command()
        if command is None:
            continue

        if "a" in command.lower():
            print("🎥 Scanning for the ball...")
            cap = cv2.VideoCapture("sample_video_2.mp4")

            while True:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Failed to grab frame.")
                    break

                detected, coords = detector.detect_ball(frame)
                if detected:
                    print(f"📍 Ball saved at {coords}")
                    break

                cv2.imshow("Scan", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            cap.release()
            cv2.destroyAllWindows()

        elif "find" in command.lower():
            print("🔍 Searching and comparing ball...")

            cap = cv2.VideoCapture("sample_video_2.mp4")

            while True:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Failed to grab frame.")
                    break

                # Save the new ball crop separately
                detected, coords = detector.detect_ball(frame, save_as_template=False, filename="found.jpg")
                if detected:
                    matched, match_coords = detector.compare_balls("ball.jpg", "found.jpg")
                    if matched:
                        print(f"✅ Matched at {match_coords}")
                        detector.engine.say("Found the same ball!")
                        detector.engine.runAndWait()
                    else:
                        print("❌ Another ball detected - no match.")
                        detector.engine.say("This is not the same ball.")
                        detector.engine.runAndWait()
                    break

                cv2.imshow("Find", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            cap.release()
            cv2.destroyAllWindows()

        elif "d" in command.lower():
            print("👋 Exiting program...")
            break

if __name__ == "__main__":
    main()