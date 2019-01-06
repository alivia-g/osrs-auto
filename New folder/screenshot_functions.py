import cv2

def load_screenshot(im):
  im.save('screenshot.png', 'PNG')
  return cv2.imread('screenshot.png', 0)

def opencv_screenshot():
  im = capture_window()
  return load_screenshot(im)