from mss import mss
import pretty_errors
import time
from PIL import ImageGrab, Image
import numpy as np
import cv2

import pyautogui
pyautogui.PAUSE = 0


def take_screenshot():
    # 0.430279016494751s

    left, top = 0, 120
    width, height = 890, 2000

    img = ImageGrab.grab(bbox=(left, top, width, height))
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    return frame


def capture_screenshot():
    # 0.0998830795288086s

    left, top = 0, 120/2
    width, height = 890/2, 2000/2

    with mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}

        screenshot = np.array(sct.grab(monitor))

        return cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)


def screenshot():
    # 0.5942399501800537s

    left, top = 0, 120
    width, height = 890, 2000

    img = pyautogui.screenshot(region=(left, top, width, height))

    return cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)


def capture_line():
    # 0.07565474510192871s

    left, top = 0, 600/2
    width, height = 890/2, 1

    with mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}

        screenshot = np.array(sct.grab(monitor))

        return cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)


def detect_circle(gray_img):
    # 0.03366827964782715s

    circles = cv2.HoughCircles(
        gray_img, cv2.HOUGH_GRADIENT, 1, 100, param1=30, param2=50, minRadius=70, maxRadius=100)

    if circles is None or len(circles) != 1:
        return None

    return circles[0][0]


def click_circle(circle):

    if circle is None:
        return

    left, top = 0, 120
    width, height = 890, 2000

    x_og, y_og, r = circle

    y = y_og + (y_og - (height/2)) * 2*r/height

    x = x_og + (x_og - width/2) * 2*r/width

    pyautogui.moveTo((x+left)/2, (y+top)/2)
    pyautogui.click()

    # y = y_og - (y_og - (height/2)) * 2*r/height

    # x = x_og - (x_og - width/2) * 2*r/width

    # pyautogui.moveTo((x+left)/2, (y+top)/2)
    # pyautogui.click()


def main():

    # start = time.time()
    img = capture_screenshot()
    # print(time.time() - start)

    # start = time.time()
    # img = take_screenshot()
    # print(time.time() - start)

    # start = time.time()
    # img = screenshot()
    # print(time.time() - start)

    # start = time.time()
    circle = detect_circle(img)
    # print(time.time() - start)

    click_circle(circle)

    # start = time.time()
    # img = capture_line()
    # print(time.time() - start)


if __name__ == '__main__':

    while True:
        main()
