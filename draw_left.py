import cv2
import numpy as np
import mediapipe as mp

# Khởi tạo MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Màu vẽ và canvas
draw_color = (255, 0, 255)
canvas = None
cap = cv2.VideoCapture(0)
xp, yp = 0, 0

def fingers_up(lm_list):
    fingers = []

    # Ngón cái: trục x
    if lm_list[4][0] > lm_list[3][0]:
        fingers.append(1)
    else:
        fingers.append(0)

    # 4 ngón còn lại: trục y
    tips = [8, 12, 16, 20]
    base = [6, 10, 14, 18]
    for tip, b in zip(tips, base):
        if lm_list[tip][1] < lm_list[b][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            # Kiểm tra số ngón đang giơ
            fingers = fingers_up(lm_list)
            total_fingers = sum(fingers)

            # Nếu giơ 5 ngón -> Xóa canvas
            if total_fingers == 5:
                canvas = np.zeros_like(frame)
                cv2.putText(frame, "CLEAR", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)

            # Nếu chỉ giơ ngón trỏ -> Vẽ
            elif fingers[1] == 1 and sum(fingers) == 1:
                x, y = lm_list[8]
                if xp == 0 and yp == 0:
                    xp, yp = x, y
                cv2.line(canvas, (xp, yp), (x, y), draw_color, 5)
                xp, yp = x, y
            else:
                xp, yp = 0, 0

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    # Hòa trộn canvas với khung hình
    frame_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(frame_gray, 20, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)
    frame = cv2.add(frame_bg, canvas_fg)

    cv2.imshow("Virtual Painter", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
