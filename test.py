import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Function to recognize hand gestures
def recognize_gesture(landmarks):
    # Gesture recognition based on landmark positions
    if landmarks:
        thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
        index_finger_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_finger_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_finger_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]
        wrist = landmarks[mp_hands.HandLandmark.WRIST]

        # 'A' Gesture: All fingers closed
        if (index_finger_tip.y > wrist.y and
                middle_finger_tip.y > wrist.y and
                ring_finger_tip.y > wrist.y and
                pinky_tip.y > wrist.y):
            return "A"

        # 'B' Gesture: All fingers extended and thumb across palm
        if (index_finger_tip.y < wrist.y and
                middle_finger_tip.y < wrist.y and
                ring_finger_tip.y < wrist.y and
                pinky_tip.y < wrist.y and
                thumb_tip.x < index_finger_tip.x):
            return "B"

        # 'C' Gesture: Fingers and thumb form a 'C' shape
        if (index_finger_tip.x < middle_finger_tip.x and
                middle_finger_tip.x < ring_finger_tip.x and
                ring_finger_tip.x < pinky_tip.x and
                thumb_tip.y < wrist.y):
            return "C"

        # 'Yes' Gesture: Thumb up
        if (thumb_tip.y < index_finger_tip.y and
                thumb_tip.y < middle_finger_tip.y):
            return "Yes"

        # 'No' Gesture: Index finger extended, others closed
        if (index_finger_tip.y < wrist.y and
                middle_finger_tip.y > wrist.y and
                ring_finger_tip.y > wrist.y and
                pinky_tip.y > wrist.y):
            return "No"

        # 'I love you' Gesture: Thumb, index, and pinky extended
        if (thumb_tip.y < wrist.y and
                index_finger_tip.y < wrist.y and
                middle_finger_tip.y > wrist.y and
                ring_finger_tip.y > wrist.y and
                pinky_tip.y < wrist.y):
            return "I love you"

    return "Unknown"

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convert the BGR image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Process the image and detect hands
    results = hands.process(image)

    # Convert the RGB image back to BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Draw hand landmarks and recognize gestures
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Recognize gesture
            gesture = recognize_gesture(hand_landmarks.landmark)
            cv2.putText(image, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the image
    cv2.imshow('Hand Gesture Recognition', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()