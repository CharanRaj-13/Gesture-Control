import cv2
import numpy as np
import mediapipe as mp
import screen_brightness_control as sbc
from math import hypot
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import pyautogui  # For controlling the mouse and clicks
import time  # For handling double-click timing


def main():
    # Volume control setup using Pycaw
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volRange = volume.GetVolumeRange()
    minVol, maxVol, _ = volRange

    # Hand detection setup using MediaPipe
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75,
        max_num_hands=2
    )
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    screen_width, screen_height = pyautogui.size()

    last_click_time = 0  # Track the time of the last click

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)  # Mirror the frame
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            left_landmark_list, right_landmark_list = get_left_right_landmarks(frame, processed, draw, mpHands)

            # Brightness control with left hand
            if left_landmark_list:
                left_distance = get_distance_for_control(frame, left_landmark_list)
                brightness_level = np.interp(left_distance, [50, 180], [0, 100])
                sbc.set_brightness(int(brightness_level))
                cv2.putText(frame, f'Brightness: {int(brightness_level)}%', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Volume and Cursor control with right hand
            if right_landmark_list:
                index_finger_tip = right_landmark_list[1]  # Index finger tip (landmark 8)
                middle_finger_tip = right_landmark_list[2]  # Middle finger tip (landmark 12)
                thumb_tip = right_landmark_list[0]  # Thumb tip (landmark 4)

                # Calculate the distance between index and middle fingers
                finger_distance = get_distance_between_fingers(frame, index_finger_tip, middle_finger_tip)

                # Cursor control (Index and Middle fingers close)
                if finger_distance < 40:
                    x_screen = np.interp(index_finger_tip[0], [0, frame.shape[1]], [0, screen_width])
                    y_screen = np.interp(index_finger_tip[1], [0, frame.shape[0]], [0, screen_height])
                    pyautogui.moveTo(int(x_screen), int(y_screen))
                    cv2.putText(frame, 'Cursor Mode', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    # Check for Left Click (Index finger and Thumb close)
                    if get_distance_between_fingers(frame, index_finger_tip, thumb_tip) < 30:
                        current_time = time.time()
                        if current_time - last_click_time < 0.5:  # Double-click threshold (500 milliseconds)
                            pyautogui.doubleClick()
                            cv2.putText(frame, 'Double Click', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        else:
                            pyautogui.click()
                            cv2.putText(frame, 'Left Click', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        last_click_time = current_time

                    # Check for Right Click (Middle finger and Thumb close)
                    elif get_distance_between_fingers(frame, middle_finger_tip, thumb_tip) < 30:
                        pyautogui.click(button='right')
                        cv2.putText(frame, 'Right Click', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                else:  # Volume control when fingers are far apart
                    right_distance = get_distance_for_control(frame, right_landmark_list)
                    vol = np.interp(right_distance, [50, 180], [minVol, maxVol])
                    volume.SetMasterVolumeLevel(vol, None)
                    vol_percentage = np.interp(right_distance, [50, 180], [0, 100])
                    cv2.putText(frame, f'Volume: {int(vol_percentage)}%', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow('Hand Gesture Control', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


def get_left_right_landmarks(frame, processed, draw, mpHands):
    left_landmark_list = []
    right_landmark_list = []

    if processed.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(processed.multi_hand_landmarks, processed.multi_handedness):
            hand_label = handedness.classification[0].label  # 'Left' or 'Right'
            draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

            # Collect landmarks for thumb (landmark 4), index (landmark 8), and middle finger (landmark 12)
            landmarks = []
            for idx, landmark in enumerate(hand_landmarks.landmark):
                height, width, _ = frame.shape
                x, y = int(landmark.x * width), int(landmark.y * height)
                if idx in [4, 8, 12]:  # Thumb, index finger tip, and middle finger tip
                    landmarks.append([x, y])

            if landmarks:
                if hand_label == 'Left':
                    left_landmark_list = landmarks
                elif hand_label == 'Right':
                    right_landmark_list = landmarks

    return left_landmark_list, right_landmark_list


def get_distance_for_control(frame, landmark_list):
    """ Calculate the distance between two control points for brightness or volume control. """
    if len(landmark_list) < 2:
        return 0
    (x1, y1), (x2, y2) = (landmark_list[0][0], landmark_list[0][1]), (landmark_list[1][0], landmark_list[1][1])
    cv2.circle(frame, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
    cv2.circle(frame, (x2, y2), 7, (255, 0, 255), cv2.FILLED)
    cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 50), 3)
    distance = hypot(x2 - x1, y2 - y1)
    return distance


def get_distance_between_fingers(frame, finger1, finger2):
    """ Calculate the distance between two fingers. """
    (x1, y1) = finger1
    (x2, y2) = finger2
    cv2.circle(frame, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
    cv2.circle(frame, (x2, y2), 7, (255, 0, 255), cv2.FILLED)
    cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 50), 3)
    distance = hypot(x2 - x1, y2 - y1)
    return distance


if __name__ == '__main__':
    main()
