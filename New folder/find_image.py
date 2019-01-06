import cv2
import templates

# methods: cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED
def find_image(input, template, method=cv2.TM_CCORR_NORMED, save_plot=True):
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
  
  x,y = top_left
  w,h = template.shape[::-1]
  bottom_right = (x + w, y + h)
  
  if save_plot:
    cv2.rectangle(input, top_left, bottom_right, 255, 2)
    cv2.imwrite('find_image.png', input)
  
  center = (x + w // 2, y + h // 2)
  return center, score

# input = cv2.imread('screenshot.png', 0)
# template = cv2.imread('attack_menu.png', 0)

# input = opencv_screenshot()
# template = templates.ATTACK_MENU
# xy, score = find_image(input, template)