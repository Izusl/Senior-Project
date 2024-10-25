# Install OpenCV if not already installed
try:
    import cv2
except ImportError:
    import os
    os.system('pip install opencv-python')
    import cv2

# Install numpy if not already installed
try:
    import numpy as np
except ImportError:
    import os
    os.system('pip install numpy')
    import numpy as np

import time
import threading

# Install DeepFace if not already installed
try:
    from deepface import DeepFace  # Using DeepFace for facial emotion recognition
except ImportError:
    import os
    os.system('pip install deepface')
    from deepface import DeepFace

# Install pynput if not already installed
try:
    from pynput import keyboard, mouse
except ImportError:
    import os
    os.system('pip install pynput')
    from pynput import keyboard, mouse

# Emotion labels for classification
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Initialize OpenCV face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Global variables to track keyboard/mouse rhythm and camera activation
camera_active = False
emotion_change_detected = False
activity_counter = 0
last_activity_time = time.time()

# Monitor keyboard and mouse activity
def on_activity():
    global activity_counter, last_activity_time, emotion_change_detected
    current_time = time.time()
    # Check if activity frequency suggests a change in user state
    if current_time - last_activity_time < 0.5:
        activity_counter += 1
    else:
        activity_counter = 1  # Reset if activity is slow
    last_activity_time = current_time

    # Detect change in rhythm
    if activity_counter > 5:  # Example threshold for detecting emotional change
        emotion_change_detected = True
        print("Emotion change detected based on activity rhythm.")

# Keyboard and mouse listeners
def keyboard_listener():
    with keyboard.Listener(on_press=lambda _: on_activity()) as listener:
        listener.join()

def mouse_listener():
    with mouse.Listener(on_click=lambda _, __, ___, ____: on_activity()) as listener:
        listener.join()

# Start monitoring in separate threads
threading.Thread(target=keyboard_listener, daemon=True).start()
threading.Thread(target=mouse_listener, daemon=True).start()

# Analyze emotions for 8 seconds
def analyze_emotions():
    global camera_active, emotion_change_detected
    cap = cv2.VideoCapture(0)

    emotion_scores = {label: 0.0 for label in emotion_labels}
    frame_count = 0
    start_time = time.time()

    while time.time() - start_time < 8:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces using OpenCV
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=7, minSize=(50, 50))

        if len(faces) == 0:
            print("No faces detected.")
            continue

        for (x, y, w, h) in faces:
            # Draw rectangle around the detected face for visual feedback
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Extract the region of interest (ROI) from the frame
            roi = frame[y:y + h, x:x + w]
            roi = cv2.resize(roi, (224, 224))  # Resize to improve quality for analysis

            # Use DeepFace to detect emotions directly from the ROI
            try:
                results = DeepFace.analyze(roi, actions=['emotion'], enforce_detection=False)

                # Handle if results is a list
                if isinstance(results, list):
                    results = results[0]

                # Get the emotions dictionary from the analysis
                emotions = results.get('emotion', {})

                # Accumulate the emotion scores
                for emotion, score in emotions.items():
                    if emotion.capitalize() in emotion_scores:
                        emotion_scores[emotion.capitalize()] += score

                frame_count += 1
                print(f"Detected emotions: {emotions}")
            except Exception as e:
                print(f"Error during analysis: {e}")

        # Show the frame with detected faces
        cv2.imshow('Emotion Recognition', frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object
    cap.release()
    cv2.destroyAllWindows()

    # Calculate average scores
    if frame_count > 0:
        for emotion in emotion_scores:
            emotion_scores[emotion] = (emotion_scores[emotion] / frame_count)

    # Display the final emotion analysis
    print("Emotion analysis over 8 seconds:")
    for emotion, percentage in emotion_scores.items():
        print(f"{emotion}: {percentage:.2f}%")

    # Reset the flags
    camera_active = False
    emotion_change_detected = False

# Main loop to check activity and activate camera
while True:
    if emotion_change_detected and not camera_active:
        camera_active = True
        analyze_emotions()
