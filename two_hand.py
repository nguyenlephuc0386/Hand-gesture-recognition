import cv2
import mediapipe as mp
import math

# Khởi tạo MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

def count_fingers(hand_landmarks, handedness):
    """
    Đếm số ngón tay giơ lên
    hand_landmarks: các điểm đánh dấu trên bàn tay
    handedness: tay trái hay tay phải
    """
    fingers = []
    
    # Xác định tay trái hay phải
    is_right_hand = handedness == "Right"
    
    # Kiểm tra ngón cái
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    
    # Ngón cái: so sánh vị trí ngang (x)
    if is_right_hand:
        if thumb_tip.x < thumb_ip.x < thumb_mcp.x:
            fingers.append(1)
        else:
            fingers.append(0)
    else:
        if thumb_tip.x > thumb_ip.x > thumb_mcp.x:
            fingers.append(1)
        else:
            fingers.append(0)
    
    # Kiểm tra 4 ngón còn lại (trỏ, giữa, áp út, út)
    finger_tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    
    finger_pips = [
        mp_hands.HandLandmark.INDEX_FINGER_PIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_PIP,
        mp_hands.HandLandmark.PINKY_PIP
    ]
    
    for tip, pip in zip(finger_tips, finger_pips):
        # Ngón giơ lên khi đầu ngón (tip) cao hơn khớp giữa (pip)
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)
    
    return fingers

# Mở webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("Nhấn 'q' để thoát chương trình")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Không thể đọc từ webcam")
        break
    
    # Lật ảnh để hiển thị như gương
    frame = cv2.flip(frame, 1)
    
    # Chuyển BGR sang RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Xử lý ảnh với MediaPipe
    results = hands.process(rgb_frame)
    
    total_fingers = 0
    
    # Vẽ và đếm ngón tay
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            # Vẽ các điểm đánh dấu trên tay
            mp_drawing.draw_landmarks(
                frame, 
                hand_landmarks, 
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )
            
            # Đếm ngón tay
            hand_label = handedness.classification[0].label
            fingers = count_fingers(hand_landmarks, hand_label)
            finger_count = sum(fingers)
            total_fingers += finger_count
            
            # Hiển thị số ngón tay của từng bàn tay
            h, w, c = frame.shape
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            x, y = int(wrist.x * w), int(wrist.y * h)
            
            cv2.putText(frame, f"{hand_label}: {finger_count}", 
                       (x - 50, y + 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (255, 255, 0), 2)
    
    # Hiển thị tổng số ngón tay
    cv2.rectangle(frame, (10, 10), (300, 80), (0, 0, 0), -1)
    cv2.putText(frame, f"Tong: {total_fingers} ngon", 
               (20, 60), 
               cv2.FONT_HERSHEY_SIMPLEX, 
               1.5, (0, 255, 255), 3)
    
    # Hiển thị hướng dẫn
    cv2.putText(frame, "Nhan 'q' de thoat", 
               (10, frame.shape[0] - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 
               0.7, (255, 255, 255), 2)
    
    # Hiển thị khung hình
    cv2.imshow('Dem Ngon Tay', frame)
    
    # Thoát khi nhấn 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
hands.close()