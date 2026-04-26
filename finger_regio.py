import cv2
import mediapipe as mp
import os

print("Initializing hand landmarker...")
# Initialize the hand landmarker
script_dir = os.path.dirname(__file__)
hand_model_path = os.path.join(script_dir, 'hand_landmarker.task')
base_options = mp.tasks.BaseOptions(model_asset_path=hand_model_path)
options = mp.tasks.vision.HandLandmarkerOptions(base_options=base_options,
                                               num_hands=2)
hand_detector = mp.tasks.vision.HandLandmarker.create_from_options(options)
print("Hand landmarker initialized successfully")

print("Initializing face landmarker...")
# Initialize the face landmarker
face_model_path = os.path.join(script_dir, 'face_landmarker.task')
face_base_options = mp.tasks.BaseOptions(model_asset_path=face_model_path)
face_options = mp.tasks.vision.FaceLandmarkerOptions(base_options=face_base_options,
                                                    output_face_blendshapes=True,
                                                    output_facial_transformation_matrixes=True,
                                                    num_faces=1)
face_detector = mp.tasks.vision.FaceLandmarker.create_from_options(face_options)
print("Face landmarker initialized successfully")

print("Opening camera...")
cap = cv2.VideoCapture(0)
print("Program started! Look for the 'Hand & Face Tracking' window.")
print("Press ESC in the video window to exit.")

frame_count = 0
while True:
    success, img = cap.read()
    if not success:
        print("Failed to read frame")
        break

    frame_count += 1
    if frame_count % 30 == 0:  # Print every 30 frames
        print(f"Processing frame {frame_count}")

    # Convert to mediapipe Image format
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)

    # Detect hand landmarks
    hand_result = hand_detector.detect(mp_image)

    # Detect face landmarks
    face_result = face_detector.detect(mp_image)

    # Process hand detection
    if hand_result.hand_landmarks:
        print(f"Hands detected: {len(hand_result.hand_landmarks)}")
        for hand_landmarks in hand_result.hand_landmarks:
            lmList = []

            # Get image dimensions
            h, w, c = img.shape

            # Convert normalized landmarks to pixel coordinates
            for landmark in hand_landmarks:
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                lmList.append((cx, cy))

            fingers = []

            # Daumen (Thumb - different logic)
            if lmList[4][0] > lmList[3][0]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Other fingers
            tips = [8, 12, 16, 20]

            for tip in tips:
                if lmList[tip][1] < lmList[tip - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            total = sum(fingers)
            print(f"Fingers counted: {total}")

            cv2.putText(img, f"Fingers: {total}", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

            # Draw hand landmarks
            for i, landmark in enumerate(hand_landmarks):
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)

    # Process face detection
    if face_result.face_landmarks:
        print(f"Face detected: {len(face_result.face_landmarks)}")
        for face_landmarks in face_result.face_landmarks:
            # Get image dimensions
            h, w, c = img.shape

            # Draw face landmarks
            for landmark in face_landmarks:
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(img, (cx, cy), 2, (255, 0, 255), -1)  # Magenta dots for face

            # Add face detection text
            cv2.putText(img, "Face Detected", (50, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("Hand & Face Tracking", img)
    cv2.setWindowProperty("Hand & Face Tracking", cv2.WND_PROP_TOPMOST, 1)  # Bring window to front

    key = cv2.waitKey(1)
    if key & 0xFF == 27:  # Press ESC to exit
        print("ESC pressed, exiting...")
        break

print("Releasing camera and destroying windows...")
cap.release()
cv2.destroyAllWindows()
print("Program finished")