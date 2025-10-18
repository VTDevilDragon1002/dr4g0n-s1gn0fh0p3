import cv2
import mediapipe as mp
import time
import sys
print(sys.version)
# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Example mapping – you can expand this to 50+ gestures
def recognize_word(fingers):
    mapping = {
        1: "I",
        2: "Need",
        3: "Water",
        4: "Food",
        5: "Help"
        # Extend this dictionary with more gestures
    }
    return mapping.get(fingers, "")

def count_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    thumb_tip = 4
    fingers = []
    landmarks = hand_landmarks.landmark

    for tip in finger_tips:
        fingers.append(1 if landmarks[tip].y < landmarks[tip - 2].y else 0)

    # Thumb detection
    fingers.append(1 if landmarks[thumb_tip].x > landmarks[thumb_tip - 2].x else 0)
    return fingers.count(1)

cap = cv2.VideoCapture(0)
sentence = []
last_word = ""
last_time = time.time()

print("Starting Hand Sign Recognition (without voice)...")
print("Press 'ESC' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_up = count_fingers(hand_landmarks)
            word = recognize_word(fingers_up)

            if word and word != last_word:
                sentence.append(word)
                print(f"Detected word: {word}")
                last_word = word
                last_time = time.time()

    # If no gesture for 2 seconds → form sentence
    if time.time() - last_time > 2 and sentence:
        full_sentence = " ".join(sentence)
        print(f"Sentence: {full_sentence}")
        sentence = []  # reset for next sentence

    # Display on screen
    cv2.putText(frame, " ".join(sentence), (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Live Hand Sign Sentence Recognition (No Voice)", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
