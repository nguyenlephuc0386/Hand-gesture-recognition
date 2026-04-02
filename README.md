# Hand Gesture Recognition Applications (Vietnamese below)

This project consists of two Python applications that use **OpenCV** and **MediaPipe Hands** for real-time hand gesture recognition through a webcam. The first script, `two_hand.py`, is designed for counting the number of raised fingers detected from up to two hands, and the second script, `game.py`, is a hand-controlled obstacle avoidance game where the player interacts with the game using hand gestures.

Both applications leverage **MediaPipe Hands** for hand landmark detection, along with **OpenCV** for capturing video from the webcam, processing frames and displaying results.

---

## Features

### 1. Finger Counting Application (`two_hand.py`)

This script uses the webcam to track the hands and count the number of raised fingers. Key features include:
- Detecting **up to two hands** in real time.
- Counting the number of **raised fingers** for each hand, separately.
- Displaying:
  - Finger count for each detected hand.
  - Total number of raised fingers from both hands.
- Drawing hand landmarks and connections on the video frame, giving a visual representation of the detected hand.
- Real-time feedback with the total finger count displayed on the screen.
- Press **`q`** to quit the program.

### 2. Hand-Controlled Obstacle Avoidance Game (`game.py`)

This script is a simple interactive game where the player controls a character on the screen with their hand gestures:
- Uses **the index finger** to control the player’s position, moving around the screen to avoid falling obstacles.
- Obstacles spawn randomly at the top of the screen and fall down at an increasing speed as the game progresses.
- **Collision detection**: if the player’s character collides with an obstacle, the game ends, and a **Game Over** screen is displayed.
- The game allows the player to restart the game by holding **five fingers** visible to the webcam for a brief moment.
- The **score** is based on the player's survival time, with difficulty increasing as the score grows.
- Press **`q`** to quit the game.

---

## Libraries Used

This project uses the following libraries:
- **OpenCV**: Library for computer vision, used for capturing video, displaying frames, and processing image data.
- **MediaPipe**: Google's library for hand tracking, used to detect hand landmarks and count raised fingers.
- Standard Python libraries:
  - `math`: Used in `two_hand.py` for mathematical calculations.
  - `random`: Used in `game.py` to randomly generate obstacles.
  - `time`: Used in `game.py` for tracking the game's time and score.

---

## Installation

Before running the applications, you need to install the required libraries. You can install them using **pip**:

```bash
pip install opencv-python mediapipe
```
---
---
# Vietnamese
# Ứng dụng nhận diện cử chỉ tay

Dự án này gồm hai ứng dụng Python sử dụng **OpenCV** và **MediaPipe Hands** để nhận diện cử chỉ tay theo thời gian thực thông qua webcam. Tập lệnh đầu tiên, `two_hand.py`, được thiết kế để đếm số ngón tay giơ lên được phát hiện từ tối đa hai bàn tay. Tập lệnh thứ hai, `game.py`, là một trò chơi né chướng ngại vật điều khiển bằng tay, trong đó người chơi tương tác với trò chơi bằng cử chỉ tay.

Cả hai ứng dụng đều sử dụng **MediaPipe Hands** để phát hiện các mốc bàn tay, kết hợp với **OpenCV** để thu hình từ webcam, xử lý khung hình và hiển thị kết quả.

---

## Tính năng

### 1. Ứng dụng đếm ngón tay (`two_hand.py`)

Tập lệnh này sử dụng webcam để theo dõi bàn tay và đếm số ngón tay đang giơ lên. Các tính năng chính bao gồm:
- Phát hiện **tối đa hai bàn tay** theo thời gian thực.
- Đếm số **ngón tay giơ lên** của từng bàn tay, riêng biệt.
- Hiển thị:
  - Số ngón tay của mỗi bàn tay được phát hiện.
  - Tổng số ngón tay giơ lên của cả hai bàn tay.
- Vẽ các mốc bàn tay và các đường kết nối trên khung hình video, giúp trực quan hóa bàn tay được phát hiện.
- Phản hồi theo thời gian thực với tổng số ngón tay được hiển thị trên màn hình.
- Nhấn **`q`** để thoát chương trình.

### 2. Trò chơi né chướng ngại vật điều khiển bằng tay (`game.py`)

Tập lệnh này là một trò chơi tương tác đơn giản, trong đó người chơi điều khiển nhân vật trên màn hình bằng cử chỉ tay:
- Sử dụng **ngón trỏ** để điều khiển vị trí của người chơi, di chuyển trên màn hình để né các chướng ngại vật rơi xuống.
- Chướng ngại vật xuất hiện ngẫu nhiên ở phía trên màn hình và rơi xuống với tốc độ tăng dần khi trò chơi tiếp diễn.
- **Phát hiện va chạm**: nếu nhân vật của người chơi va chạm với chướng ngại vật, trò chơi kết thúc và màn hình **Game Over** sẽ được hiển thị.
- Trò chơi cho phép người chơi khởi động lại bằng cách giữ **năm ngón tay (một bàn tay)** trước webcam trong một khoảng thời gian ngắn.
- **Điểm số** được tính dựa trên thời gian sống sót của người chơi, với độ khó tăng dần khi điểm số tăng.
- Nhấn **`q`** để thoát trò chơi.

---

## Các thư viện sử dụng

Dự án này sử dụng các thư viện sau:
- **OpenCV**: Thư viện thị giác máy tính, dùng để thu video, hiển thị khung hình và xử lý dữ liệu hình ảnh.
- **MediaPipe**: Thư viện của Google dùng để theo dõi bàn tay, được sử dụng để phát hiện các mốc bàn tay và đếm số ngón tay giơ lên.
- Các thư viện Python tiêu chuẩn:
  - `math`: Được sử dụng trong `two_hand.py` cho các phép tính toán học.
  - `random`: Được sử dụng trong `game.py` để tạo chướng ngại vật ngẫu nhiên.
  - `time`: Được sử dụng trong `game.py` để theo dõi thời gian chơi và điểm số.

---

## Cài đặt

Trước khi chạy các ứng dụng, bạn cần cài đặt các thư viện cần thiết. Bạn có thể cài đặt chúng bằng **pip**:

```bash
pip install opencv-python mediapipe
