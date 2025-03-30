# Hand Gesture Based System Control

This project implements a real-time hand gesture recognition system to control various computer functions, including volume, screen brightness, and mouse cursor movement, using a webcam.

## Overview

The application utilizes MediaPipe for hand tracking, Pycaw for volume control, screen_brightness_control for brightness adjustment, and PyAutoGUI for mouse control. By analyzing hand gestures captured by the webcam, the system allows users to interact with their computer in an intuitive and hands-free manner.

## Features

* **Volume Control:** Adjust system volume by varying the distance between the thumb and index finger of the right hand.
* **Brightness Control:** Modify screen brightness by varying the distance between the thumb and index finger of the left hand.
* **Mouse Cursor Control:** Move the mouse cursor by moving the index finger of the right hand when the index and middle fingers are close together.
* **Left Click:** Perform a left mouse click by bringing the thumb and index finger of the right hand close together. Double click is also supported.
* **Right Click:** Perform a right mouse click by bringing the thumb and middle finger of the right hand close together.
* **Real-time Processing:** Processes hand gestures in real-time for smooth and responsive control.

## Technologies Used

* **OpenCV (cv2):** For capturing and processing webcam video.
* **MediaPipe (mediapipe):** For real-time hand tracking and landmark detection.
* **NumPy (numpy):** For numerical operations and data manipulation.
* **Pycaw (pycaw):** For controlling system volume.
* **screen_brightness_control (screen_brightness_control):** For adjusting screen brightness.
* **PyAutoGUI (pyautogui):** For mouse control and simulating clicks.
* **Math (math.hypot):** For calculating distances between landmarks.
* **Time (time):** For managing double click timing.
* **ctypes, comtypes:** Used for interacting with audio api's.

## Prerequisites

Before running the application, ensure you have the following installed:

* Python 3.x
* Required Python packages:

    ```bash
    pip install opencv-python mediapipe numpy pycaw screen_brightness_control pyautogui
    ```
    If you have issues with pycaw, ensure you have the correct dependencies for windows.
## Getting Started

1.  **Clone the repository:**

    ```bash
    git clone [repository_url]
    ```

2.  **Navigate to the project directory:**

    ```bash
    cd [project_directory]
    ```

3.  **Run the Python script:**

    ```bash
    python main.py
    ```

4.  **Usage:**
    * **Volume Control:** Raise or lower the right hand and vary the distance between your thumb and index finger.
    * **Brightness Control:** Raise or lower the left hand and vary the distance between your thumb and index finger.
    * **Mouse Cursor:** Close your right index and middle fingers, and move your index finger to move the cursor.
    * **Left Click:** Close your right thumb and index finger. A double click is registered if the action happens quickly.
    * **Right Click:** Close your right thumb and middle finger.
    * Press 'q' to quit the application.

## Code Explanation

* `main()`: Initializes the webcam, hand tracking, and control modules. Processes frames from the webcam, detects hand gestures, and controls system functions.
* `get_left_right_landmarks()`: Detects hand landmarks and separates them into left and right hands.
* `get_distance_for_control()`: Calculates the distance between two landmarks for volume and brightness control.
* `get_distance_between_fingers()`: Calculates the distance between two fingers for mouse control and click detection.

## Notes

* Ensure proper lighting conditions for accurate hand tracking.
* Adjust the distance thresholds and sensitivity parameters as needed for optimal performance.
* The performance might vary depending on your webcam quality and computer processing power.
* This code has been developed and tested on Windows. Some features may not work on other operating systems without modifications.
* Ensure that your webcam is connected and functioning correctly.
* This code is meant to be a starting point. Feel free to modify and expand its functionality.

## Author

* CharanRaj-13

## License

