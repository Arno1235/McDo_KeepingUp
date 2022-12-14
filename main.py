from mss import mss
from PIL import ImageGrab
import numpy as np
import cv2

import pyautogui
pyautogui.PAUSE = 0

LEFT, TOP = 0, 120
WIDTH, HEIGHT = 890, 2000


def show_screenshot():

    img = ImageGrab.grab(bbox=(LEFT, TOP, WIDTH, HEIGHT))
    img.show()


def capture_screenshot():

    with mss() as sct:
        monitor = {"top": TOP/2, "left": LEFT/2,
                   "width": WIDTH/2, "height": HEIGHT/2}
        screenshot = np.array(sct.grab(monitor))

        return cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)


def detect_circle(gray_img):

    circles = cv2.HoughCircles(
        gray_img, cv2.HOUGH_GRADIENT, 1, 100, param1=30, param2=50, minRadius=70, maxRadius=100)

    if circles is None or len(circles) != 1:
        return None

    return circles[0][0]


def click_circle(circle):

    if circle is None:
        return

    x_og, y_og, r = circle

    y = y_og + (y_og - (HEIGHT/2)) * 2*r/HEIGHT

    x = x_og + (x_og - WIDTH/2) * 2*r/WIDTH

    pyautogui.moveTo((x+LEFT)/2, (y+TOP)/2)
    pyautogui.click()


def main():

    img = capture_screenshot()

    circle = detect_circle(img)

    click_circle(circle)


if __name__ == '__main__':

    # show_screenshot()

    while True:
        main()
