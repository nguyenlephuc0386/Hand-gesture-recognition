import cv2
import mediapipe as mp

# Khởi tạo mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Camera
cap = cv2.VideoCapture(0)

# Chỉ số các đầu ngón tay
tip_ids = [4, 8, 12, 16, 20]

def count_fingers(hand_landmarks, hand_label):
    fingers = []

    # Thumb: xét theo trục X (ngón cái ngang)
    if hand_label == "Right":
        if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)
    else:  # Left hand
        if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

    # Các ngón còn lại: xét theo trục Y (ngón dựng lên cao hơn khớp giữa)
    for i in range(1, 5):
        if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            label = handedness.classification[0].label  # 'Left' or 'Right'

            # Đếm ngón tay giơ lên
            count = count_fingers(hand_landmarks, label)

            # Vẽ các điểm và kết nối
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Lấy tọa độ cổ tay để hiển thị số
            cx = int(hand_landmarks.landmark[0].x * w)
            cy = int(hand_landmarks.landmark[0].y * h)

            # Hiển thị thông tin lên màn hình
            cv2.putText(frame, f"{label} hand: {count}", (cx - 50, cy - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

    cv2.imshow("Hand Gesture Recognition", frame)

    # Nhấn phím 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng
cap.release()
cv2.destroyAllWindows()
