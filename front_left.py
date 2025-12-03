# Import thư viện
import cv2
import mediapipe as mp

# Khởi tạo MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Mở webcam
cap = cv2.VideoCapture(0)

# Danh sách các điểm đầu ngón tay
tip_ids = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read() # Lấy ảnh từ webcam
    img = cv2.flip(img, 1)  # Lật ảnh để giống gương
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    fingers_up = 0
    
    # Phát hiện bàn tay
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            # Kiểm tra ngón cái
            if lm_list[tip_ids[0]][0] > lm_list[tip_ids[0] - 1][0]:
                fingers_up += 1

            # Kiểm tra các ngón còn lại
            for i in range(1, 5):
                if lm_list[tip_ids[i]][1] < lm_list[tip_ids[i] - 2][1]:
                    fingers_up += 1

            # Vẽ khung tay
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Hiển thị số ngón tay
    cv2.putText(img, f'So ngon tay: {fingers_up}', (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    # Mở cửa sổ hiển thị video, nhấn q để thoát
    cv2.imshow("Hand Gesture", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Tắt webcam và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()
