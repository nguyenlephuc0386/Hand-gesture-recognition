import cv2
import mediapipe as mp
import random
import time

# Khởi tạo MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player_x = width // 2
        self.player_y = height - 100
        self.player_radius = 20
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.obstacle_speed = 5
        self.spawn_rate = 60  # Frames giữa mỗi chướng ngại vật
        self.frame_count = 0
        self.start_time = time.time()
        
    def spawn_obstacle(self):
        """Tạo chướng ngại vật mới"""
        x = random.randint(30, self.width - 30)
        y = -20
        width = random.randint(40, 80)
        height = random.randint(40, 80)
        self.obstacles.append({'x': x, 'y': y, 'w': width, 'h': height})
    
    def update(self):
        """Cập nhật trạng thái game"""
        if self.game_over:
            return
        
        self.frame_count += 1
        
        # Tạo chướng ngại vật mới
        if self.frame_count % self.spawn_rate == 0:
            self.spawn_obstacle()
        
        # Di chuyển chướng ngại vật
        for obs in self.obstacles:
            obs['y'] += self.obstacle_speed
        
        # Xóa chướng ngại vật ra khỏi màn hình
        self.obstacles = [obs for obs in self.obstacles if obs['y'] < self.height + 50]
        
        # Kiểm tra va chạm
        for obs in self.obstacles:
            if self.check_collision(obs):
                self.game_over = True
                return
        
        # Tăng điểm
        self.score = int(time.time() - self.start_time)
        
        # Tăng độ khó theo thời gian
        if self.score > 0 and self.score % 10 == 0:
            self.obstacle_speed = min(5 + self.score // 10, 15)
            self.spawn_rate = max(30, 60 - self.score // 5)
    
    def check_collision(self, obs):
        """Kiểm tra va chạm giữa người chơi và chướng ngại vật"""
        # Va chạm hình tròn với hình chữ nhật
        closest_x = max(obs['x'] - obs['w']//2, min(self.player_x, obs['x'] + obs['w']//2))
        closest_y = max(obs['y'] - obs['h']//2, min(self.player_y, obs['y'] + obs['h']//2))
        
        distance_x = self.player_x - closest_x
        distance_y = self.player_y - closest_y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        
        return distance < self.player_radius
    
    def move_player(self, x, y):
        """Di chuyển người chơi"""
        self.player_x = max(self.player_radius, min(x, self.width - self.player_radius))
        self.player_y = max(self.player_radius, min(y, self.height - self.player_radius))
    
    def draw(self, frame):
        """Vẽ game lên frame"""
        # Vẽ nền
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (self.width, self.height), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
        if not self.game_over:
            # Vẽ người chơi
            cv2.circle(frame, (self.player_x, self.player_y), 
                      self.player_radius, (0, 255, 0), -1)
            cv2.circle(frame, (self.player_x, self.player_y), 
                      self.player_radius, (0, 200, 0), 3)
            
            # Vẽ chướng ngại vật
            for obs in self.obstacles:
                cv2.rectangle(frame, 
                            (obs['x'] - obs['w']//2, obs['y'] - obs['h']//2),
                            (obs['x'] + obs['w']//2, obs['y'] + obs['h']//2),
                            (0, 0, 255), -1)
                cv2.rectangle(frame, 
                            (obs['x'] - obs['w']//2, obs['y'] - obs['h']//2),
                            (obs['x'] + obs['w']//2, obs['y'] + obs['h']//2),
                            (0, 0, 200), 3)
            
            # Hiển thị điểm số
            cv2.putText(frame, f"Diem: {self.score}", 
                       (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                       1.2, (255, 255, 255), 3)
            cv2.putText(frame, f"Toc do: {self.obstacle_speed}", 
                       (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.8, (255, 255, 255), 2)
        else:
            # Màn hình Game Over
            cv2.putText(frame, "GAME OVER!", 
                       (self.width//2 - 150, self.height//2 - 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       2, (0, 0, 255), 4)
            cv2.putText(frame, f"Diem cuoi: {self.score}", 
                       (self.width//2 - 120, self.height//2 + 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       1.2, (255, 255, 255), 3)
            cv2.putText(frame, "Gio 5 ngon de choi lai", 
                       (self.width//2 - 180, self.height//2 + 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (255, 255, 0), 2)
    
    def reset(self):
        """Khởi động lại game"""
        self.player_x = self.width // 2
        self.player_y = self.height - 100
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.obstacle_speed = 5
        self.spawn_rate = 60
        self.frame_count = 0
        self.start_time = time.time()

def count_fingers(hand_landmarks, handedness):
    """Đếm số ngón tay giơ lên"""
    fingers = []
    
    is_right_hand = handedness == "Right"
    
    # Kiểm tra ngón cái
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    
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
    
    # Kiểm tra 4 ngón còn lại
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
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)
    
    return fingers

# Mở webcam
cap = cv2.VideoCapture(0)
frame_width = 1280
frame_height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

# Khởi tạo game
game = Game(frame_width, frame_height)

print("=== GAME NÉ CHƯỚNG NGẠI VẬT ===")
print("- Dùng ngón trỏ để điều khiển")
print("- Giơ 5 ngón tay để restart")
print("- Nhấn 'q' để thoát")
print("================================")

restart_timer = 0
RESTART_DELAY = 30  # Frames cần giữ 5 ngón để restart

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Không thể đọc từ webcam")
        break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    index_finger_detected = False
    five_fingers_detected = False
    
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            hand_label = handedness.classification[0].label
            fingers = count_fingers(hand_landmarks, hand_label)
            finger_count = sum(fingers)
            
            # Vẽ tay (nhạt hơn để không che game)
            mp_drawing.draw_landmarks(
                frame, 
                hand_landmarks, 
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(100, 100, 100), thickness=1, circle_radius=1),
                mp_drawing.DrawingSpec(color=(150, 150, 150), thickness=1)
            )
            
            # Kiểm tra 5 ngón để restart
            if finger_count == 5:
                five_fingers_detected = True
            
            # Lấy vị trí ngón trỏ (chỉ khi chỉ giơ ngón trỏ hoặc đang chơi)
            if fingers[1] == 1:  # Ngón trỏ giơ lên
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                x = int(index_tip.x * frame_width)
                y = int(index_tip.y * frame_height)
                
                # Vẽ dấu điều khiển
                cv2.circle(frame, (x, y), 10, (255, 255, 0), -1)
                cv2.circle(frame, (x, y), 12, (255, 200, 0), 2)
                
                # Di chuyển người chơi
                if not game.game_over:
                    game.move_player(x, y)
                    index_finger_detected = True
    
    # Xử lý restart
    if five_fingers_detected and game.game_over:
        restart_timer += 1
        # Hiển thị thanh progress
        progress = int((restart_timer / RESTART_DELAY) * 200)
        cv2.rectangle(frame, (frame_width//2 - 100, frame_height//2 + 120),
                     (frame_width//2 - 100 + progress, frame_height//2 + 140),
                     (0, 255, 0), -1)
        cv2.rectangle(frame, (frame_width//2 - 100, frame_height//2 + 120),
                     (frame_width//2 + 100, frame_height//2 + 140),
                     (255, 255, 255), 2)
        
        if restart_timer >= RESTART_DELAY:
            game.reset()
            restart_timer = 0
    else:
        restart_timer = 0
    
    # Cập nhật game
    game.update()
    game.draw(frame)
    
    # Hướng dẫn
    if not game.game_over:
        cv2.putText(frame, "Dung ngon tro de dieu khien", 
                   (frame_width - 380, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    cv2.putText(frame, "Nhan 'q' de thoat", 
               (10, frame_height - 20),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    cv2.imshow('Game Ne Chuong Ngai Vat', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()