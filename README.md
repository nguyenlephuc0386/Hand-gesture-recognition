# Hand Gesture Recognition Applications

This project consists of two Python applications that use **OpenCV** and **MediaPipe Hands** for real-time hand gesture recognition through a webcam. The first script, `two_hand.py`, is designed for counting the number of raised fingers detected from up to two hands, and the second script, `game.py`, is a hand-controlled obstacle avoidance game where the player interacts with the game using hand gestures.

Both applications leverage **MediaPipe Hands** for hand landmark detection, along with **OpenCV** for capturing video from the webcam, processing frames, and displaying results.

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

## Technologies Used

This project uses the following technologies:
- **Python**: The programming language for both applications.
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
