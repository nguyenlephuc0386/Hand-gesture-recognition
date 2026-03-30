# Hand Gesture Recognition Applications

This project includes two interactive Python applications that utilize **MediaPipe** and **OpenCV** for real-time hand tracking and gesture recognition via webcam.

## 📁 Project Structure

The project consists of two main source code files:

### 1. `two_hand.py` - Finger Counting Application
This application uses the camera to detect and track up to two hands simultaneously.
* **Features:**
  * Draws hand landmarks directly on the video feed.
  * Distinguishes between left and right hands to accurately determine the state of the thumb.
  * Counts the number of raised fingers for each hand.
  * Displays the total number of raised fingers from both hands on the screen.

### 2. `game.py` - Gesture-Controlled Obstacle Dodging Game
An interactive mini-game combining Computer Vision and basic game logic.
* **Features & Rules:**
  * **Controls:** The player uses the tip of their **index finger** to control a character (the green circle) on the screen.
  * **Objective:** Dodge the falling obstacles (the red blocks).
  * **Difficulty:** The speed and spawn rate of the obstacles dynamically increase over time as your score gets higher.
  * **Restart:** Upon Game Over, the player simply needs to **raise all 5 fingers** and hold them for a short duration to fill the progress bar and automatically restart the game.

---

## 🛠️ Prerequisites & Installation

To run these scripts, you need **Python** (version 3.7+ recommended) and a working webcam.

**Step 1:** Clone or download the source code to your local machine.

**Step 2:** Open your terminal or command prompt and install the required libraries using `pip`:

```bash
pip install opencv-python mediapipe
