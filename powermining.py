import time
time.sleep(2)
import lib
import constants

if __name__ == '__main__':
    ROCK_COLORS = (constants.COPPER_ROCK_COLOR, constants.TIN_ROCK_COLOR)

    lib.delay(2)
    #while True:
    for i in range(500):
        rock_coords = lib.find_color(ROCK_COLORS[i % 2])
        if rock_coords is None:
            continue
        x, y = rock_coords
        lib.move_click("right", x, y)
        lib.move_click("left", x - 38, y + 33)
        lib.delay(5)
        lib.move_click("right", 601, 217)
        lib.move_click("left", 578, 258)
        # lib.delay(1)
        lib.rotate_camera(0.5, 'left')