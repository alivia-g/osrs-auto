import cv2
import keyboard
import math
import pyautogui
import pyscreenshot as ImageGrab
import random
import sys
import time
import win32gui


def find_app_window(title="OSBuddy Guest - Guest"):
    # window_id = win32gui.FindWindowEx(None, None, None, title)
    window_id = win32gui.FindWindow(None, title)
    # print(window_id)
    coordinates = win32gui.GetWindowRect(window_id)
    return coordinates


# find 2OR window
osrs_window = find_app_window()
(x0, y0, x1, y1) = osrs_window


def capture_window():
    #print('*', x0, y0, x1, y1, '*')
    image = ImageGrab.grab(bbox=(x0, y0, x1, y1))
    return image


def load_screenshot(im):
    im.save('screenshot.png', 'PNG')
    return cv2.imread('screenshot.png')


def opencv_screenshot():
    im = capture_window()
    return load_screenshot(im)


def detect_color(row, col):
    im = capture_window()
    pix = im.load()
    #pix = capture_window().load()
    #for r in range(height):
     #   for c in range(width):
            #print(pix[r, c])
    return pix[row, col]


# check color similarity (Manhattan Distance)
def manhattan_distance(c1, c2):  # color1 and color2
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])


def find_color(color, tolerance=0):
    im = capture_window()
    pix = im.load()
    width, height = im.size
    for c in range(width):
        for r in range(height):
            pixel_color = pix[c, r]
            distance = manhattan_distance(pixel_color, color)
            if distance <= tolerance:
                return c, r
    return None


def find_colors(color, tolerance=0):
    matched_pixels = []
    im = capture_window()
    pix = im.load()
    width, height = im.size
    for c in range(width):
        for r in range(height):
            pixel_color = pix[c, r]
            distance = manhattan_distance(pixel_color, color)
            if distance <= tolerance:
                matched_pixels.append((c, r))
    return matched_pixels


# randomly return one of the pixels that matched the color
def find_color_random(color, tolerance=0):
    matched_pixels = find_colors(color, tolerance)
    if len(matched_pixels) == 0:
        return None
    secure_rng = random.SystemRandom()
    random_pixel_coords = secure_rng.choice(matched_pixels)
    return random_pixel_coords


def count_colors(color, tolerance=0):
    list_of_pixs = find_colors(color, tolerance)
    return len(list_of_pixs)


TM_METHODS = (cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED)
TM_METHOD_NAMES = ("SqDiff", "SqDiffNormed", "CCorr", "CCorrNormed", "CCoeff", "CCoeffNormed")
# not recommended: CCorr, SqDiff [https://pythonspot.com/tag/opencv/]
# recommended: CCoeffNormed [Yeong, Yew, Chai, Suandi (2010)]

# return_coords: 'top-left', 'center', or 'rectangle'
def find_image(input, template, method=cv2.TM_CCOEFF_NORMED, save_plot=True, return_coords='center'):
    # apply template matching
    result = cv2.matchTemplate(input, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum (else maximum)
    if method in (cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED):
        top_left = min_loc
        score = min_val
    else:
        top_left = max_loc
        score = max_val

    x, y = top_left
    h, w = template.shape[:-1]
    bottom_right = (x + w, y + h)

    if save_plot:
        overlay = input.copy()
        cv2.rectangle(overlay, top_left, bottom_right, 255, 2)
        cv2.imwrite('find_image_' + TM_METHOD_NAMES[method] + '.png', overlay)

    if return_coords == 'top-left':
        return top_left, score
    elif return_coords == 'center':
        return (x + w // 2, y + h // 2), score
    elif return_coords == 'rectangle':
        return (x, y, x + w, y + h), score
    else:
        print('invalid return_coords: ', return_coords)
        return score


def open_inventory():  # match_color
    pass


def get_xy():
    absolute_coords = pyautogui.position()
    (x,y) = absolute_coords
    relative_coords = (x-x0, y-y0)
    return relative_coords


def move_mouse(x, y):
    pyautogui.moveTo(x, y)


def left_click(x=None, y=None):
    pyautogui.click(x, y, button="left")


def right_click(x=None, y=None):
    pyautogui.click(x, y, button="right")


def click_mouse(button, x=None, y=None):
    pyautogui.click(x, y, button=button)


def move_click(button, x, y):
    x += x0
    y += y0
    move_mouse(x, y)
    click_mouse(button, x, y)


def delay(duration, ms_per_iter=10):
    num_of_iters = math.ceil(duration*1000 / ms_per_iter)
    seconds = ms_per_iter / 1000
    for i in range(num_of_iters):
        time.sleep(seconds)
        if keyboard.is_pressed('q'):
            pyautogui.keyUp('left')
            pyautogui.keyUp('right')
            print('Program terminated by ZD')
            sys.exit(0)


def rotate_camera(duration, direction):
    pyautogui.keyDown(direction)
    delay(duration)
    pyautogui.keyUp(direction)


if __name__ == '__main__':
    pass