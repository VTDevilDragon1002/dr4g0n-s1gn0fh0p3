import cv2
import mediapipe as mp
import time
import pyttsx3
import sys
print(sys.executable)

engine = pyttsx3.init()
engine.say("Hello! pyttsx3 is working.")
engine.runAndWait()


# -----------------------------
# Initialize Mediapipe & Pyttsx3
# -----------------------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# -----------------------------
# Gesture Mapping (expandable)
# -----------------------------
gesture_mapping = {
     # Single-hand gestures (right hand)
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",

    # Single-hand gestures (left hand) – add 10 to distinguish
    6: "G",
    7: "H",
    8: "I",
    9: "J",
    10: "K",

    # Two-hand combinations (finger counts summed)
    11: "L",
    12: "M",
    13: "N",
    14: "O",
    15: "P",
    16: "Q",
    17: "R",
    18: "S",
    19: "T",
    20: "U",

    # Common words
    21: "Hello",
    22: "Yes",
    23: "No",
    24: "Thank You",
    25: "Please",
    26: "Sorry",
    27: "Help",
    28: "Water",
    29: "Food",
    30: "I",
    31: "You",
    32: "We",
    33: "Need",
    34: "Go",
    35: "Stop",
    36: "Come",
    37: "Wait",
    38: "Bathroom",
    39: "Good",
    40: "Bad",
    41: "Friend",
    42: "Love",
    43: "Hurry",
    44: "Sit",
    45: "Stand",
    46: "Run",
    47: "Play",
    48: "Book",
    49: "School",
    50: "Sleep"
    # Add more mappings for letters or words up to 50+ gestures
}

# -----------------------------
# Finger counting function
# -----------------------------
def count_fingers(hand_landmarks, hand_label):
    finger_tips = [8, 12, 16, 20]
    thumb_tip = 4
    fingers = []
    landmarks = hand_landmarks.landmark

    for tip in finger_tips:
        fingers.append(1 if landmarks[tip].y < landmarks[tip - 2].y else 0)

    # Thumb detection
    if hand_label == "Right":
        fingers.append(1 if landmarks[thumb_tip].x > landmarks[thumb_tip - 2].x else 0)
    else:
        fingers.append(1 if landmarks[thumb_tip].x < landmarks[thumb_tip - 2].x else 0)

    return fingers.count(1)

# -----------------------------
# Main variables
# -----------------------------
cap = cv2.VideoCapture(0)
sentence = []
current_word = ""
word_start_time = 0
last_spoken_time = 0
pause_threshold = 2    # seconds before speaking sentence
hold_threshold = 0.5   # seconds to confirm word

print("Starting Full Sign-to-Speech System...")
print("Press 'ESC' to exit.")

# -----------------------------
# Main Loop
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    detected_word = ""

    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            hand_label = handedness.classification[0].label  # 'Right' or 'Left'
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers_up = count_fingers(hand_landmarks, hand_label)
            word = gesture_mapping.get(fingers_up, "")

            if word:
                # New word detection with hold threshold
                if word != current_word:
                    current_word = word
                    word_start_time = time.time()
                elif time.time() - word_start_time >= hold_threshold:
                    if not sentence or word != sentence[-1]:
                        sentence.append(word)
                        print(f"Detected word: {word}")
                        engine.say(word)   # optional immediate speech
                        engine.runAndWait()
                        last_spoken_time = time.time()
                        detected_word = word
            else:
                current_word = ""
                word_start_time = 0

    # Speak full sentence after pause
    if sentence and time.time() - last_spoken_time > pause_threshold:
        full_sentence = " ".join(sentence)
        print(f"Full sentence: {full_sentence}")
        engine.say(full_sentence)
        engine.runAndWait()
        sentence = []
        current_word = ""
        detected_word = ""

    # Display sentence and current word
    cv2.putText(frame, " ".join(sentence + ([detected_word] if detected_word else [])),
                (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow("Full Sign-to-Speech System", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
