import templates
import lib
import constants

if __name__ == '__main__':
    ATTACKABLE_CREATURES = (constants.MALE_SKIN_TONE,
                            constants.FEMALE_SKIN_TONE,
                            constants.RED_SHIRT_WOMAN,
                            constants.BLUE_SHIRT_MAN,
                            constants.GREEN_SHIRT_MAN,
                            # constants.GOBLIN,
                            constants.PURPLE_SHIRT_WOMAN,)
    SIZE = len(ATTACKABLE_CREATURES)
    lib.delay(2)
    for i in range(10):
        lib.rotate_camera(0.5, 'left')
        target = ATTACKABLE_CREATURES[i % SIZE]
        print("Try to find", target)
        creature_coord = lib.find_color_random(target)
        if creature_coord is None:
            continue
        print("Found", target)
        x, y = creature_coord
        # lib.move_click("left", x, y)
        # lib.delay(20)
        lib.move_click("right", x, y)
        screenshot = lib.opencv_screenshot()  # get a screenshot for OpenCV
        xy, score = lib.find_image(screenshot, templates.ATTACK_MENU)  # try to find the attack text
        if score >= 0.9:  # check whether the score is above some threshold
            x, y = xy
            print("Attacking", target)
            lib.move_click("left", x, y)
            lib.delay(20)