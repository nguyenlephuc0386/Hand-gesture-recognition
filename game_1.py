# Import thư viện
import cv2
import mediapipe as mp
import pygame
import random
import sys

# Khởi tạo Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
tip_ids = [4, 8, 12, 16, 20]

# Hàm đếm số ngón tay
def count_fingers(hand_landmarks, hand_label):
    fingers = []

    # Ngón cái
    if hand_label == "Right":
        fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0] - 1].x else 0)
    else:
        fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x else 0)

    # Các ngón còn lại
    for i in range(1, 5):
        fingers.append(1 if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y else 0)

    return sum(fingers)

# Cài đặt Pygame
pygame.init()
WIDTH, HEIGHT = 640, 480 # Màn hình game 640×480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ne chuong ngai vat")
FONT = pygame.font.SysFont("Arial", 32)

# Màu
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Game objects
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - 80

obstacle_size = 50
obstacles = []
speed = 7
score = 0
game_over = False

# Mở webcam
cap = cv2.VideoCapture(0)

clock = pygame.time.Clock()

while True:
    # Xử lý sự kiện pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()

    # Xử lý camera
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    finger_count = 0
    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handedness.classification[0].label
            # Lấy ngón trỏ
            index_finger = hand_landmarks.landmark[8]
            player_x = int(index_finger.x * WIDTH)

            finger_count = count_fingers(hand_landmarks, label)

            # Vẽ bàn tay lên frame webcam
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Game logic
    if not game_over:
        # Sinh chướng ngại vật
        if random.random() < 0.02:
            obstacles.append([random.randint(0, WIDTH - obstacle_size), 0])

        # Di chuyển chướng ngại vật
        for obs in obstacles:
            obs[1] += speed

        # Kiểm tra va chạm
        player_rect = pygame.Rect(player_x - player_size//2, player_y - player_size//2, player_size, player_size)
        for obs in obstacles:
            obs_rect = pygame.Rect(obs[0], obs[1], obstacle_size, obstacle_size)
            if player_rect.colliderect(obs_rect):
                game_over = True

        score += 1

    else:
        # Restart nếu giơ 5 ngón tay
        if finger_count == 5:
            obstacles = []
            score = 0
            game_over = False

    # Vẽ game
    WIN.fill(BLACK)

    if not game_over:
        # Vẽ người chơi
        pygame.draw.rect(WIN, GREEN, player_rect)

        # Vẽ chướng ngại vật
        for obs in obstacles:
            pygame.draw.rect(WIN, RED, (obs[0], obs[1], obstacle_size, obstacle_size))

        # Vẽ điểm
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        WIN.blit(score_text, (10, 10))
    else:
        over_text = FONT.render("GAME OVER", True, RED)
        restart_text = FONT.render("Show 5 fingers to Restart", True, WHITE)
        WIN.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 50))
        WIN.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))

    pygame.display.update()
    clock.tick(30)

    # Hiển thị webcam
    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
