# possible for start you need to execute: ```xhost +```
import enum
import time
import keyboard
import pyautogui

TOOLS_POSITION_STEP_X = 55
TOOLS_POSITION_STEP_Y = 55

TOOLS_PEN_POSITION_START_X = 1110
TOOLS_PEN_POSITION_START_Y = 200 - TOOLS_POSITION_STEP_Y

TOOLS_LINE_POSITION_START_X = 1110
TOOLS_LINE_POSITION_START_Y = 310 - TOOLS_POSITION_STEP_Y


def tools_line_pos_x(deep: int):
    return TOOLS_LINE_POSITION_START_X + TOOLS_POSITION_STEP_X * deep

def tools_line_pos_y(deep: int):
    return TOOLS_LINE_POSITION_START_Y + TOOLS_POSITION_STEP_Y * deep


def tools_pen_pos_x(deep: int):
    return TOOLS_PEN_POSITION_START_X + TOOLS_POSITION_STEP_X * deep

def tools_pen_pos_y(deep: int):
    return TOOLS_PEN_POSITION_START_Y + TOOLS_POSITION_STEP_Y * deep


class Color(enum.Enum):
    black = 1
    dark = 2
    light = 3
    red = 4
    orange = 5
    olive = 6
    green = 7
    blue = 8
    purple = 9


pen_colors = {
    Color.black: pyautogui.Point(x=tools_pen_pos_x(2), y=tools_pen_pos_y(1)),
    Color.dark: pyautogui.Point(x=tools_pen_pos_x(2), y=tools_pen_pos_y(2)),
    Color.light: pyautogui.Point(x=tools_pen_pos_x(2), y=tools_pen_pos_y(3)),
    Color.red: pyautogui.Point(x=tools_pen_pos_x(2), y=tools_pen_pos_y(4)),
    Color.orange: pyautogui.Point(x=tools_pen_pos_x(2), y=tools_pen_pos_y(5)),
    Color.olive: pyautogui.Point(x=tools_pen_pos_x(2), y=tools_pen_pos_y(6)),
    Color.green: pyautogui.Point(x=tools_pen_pos_x(2), y=tools_pen_pos_y(7)),
    Color.blue: pyautogui.Point(x=tools_pen_pos_x(2), y=tools_pen_pos_y(8)),
    Color.purple: pyautogui.Point(x=tools_pen_pos_x(2), y=tools_pen_pos_y(9)),
}

pen_size = {
    1: pyautogui.Point(x=tools_pen_pos_x(3), y=tools_pen_pos_y(1)),
    2: pyautogui.Point(x=tools_pen_pos_x(3), y=tools_pen_pos_y(2)),
    3: pyautogui.Point(x=tools_pen_pos_x(3), y=tools_pen_pos_y(3)),
    4: pyautogui.Point(x=tools_pen_pos_x(3), y=tools_pen_pos_y(4)),
    5: pyautogui.Point(x=tools_pen_pos_x(3), y=tools_pen_pos_y(5)),
}

TIME_DELAY: float = 0.075

def pen_select(with_click=True):
    pyautogui.moveTo(x=tools_pen_pos_x(1), y=tools_pen_pos_y(1))
    time.sleep(TIME_DELAY)
    if with_click:
        pyautogui.click()

def line_select():
    pyautogui.moveTo(x=tools_line_pos_x(1), y=tools_line_pos_y(1))
    time.sleep(TIME_DELAY)
    pyautogui.moveTo(x=tools_line_pos_x(2), y=tools_line_pos_y(1))
    pyautogui.click()

class PenCurrentPosition:
    def __enter__(self):
        self.current_position: pyautogui.Point = pyautogui.position()
        pen_select(with_click=False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # pen_select()
        pyautogui.moveTo(self.current_position)

class LineCurrentPosition:
    def __enter__(self):
        self.current_position: pyautogui.Point = pyautogui.position()
        line_select()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # line_select()
        pyautogui.moveTo(self.current_position)

def pen_set_color(color: Color):
    with PenCurrentPosition():
        pyautogui.moveTo(x=tools_pen_pos_x(2), y=tools_pen_pos_y(color.value))
        pyautogui.leftClick()

def line_set_color(color: Color):
    with LineCurrentPosition():
        pyautogui.moveTo(x=tools_line_pos_x(3), y=tools_line_pos_y(color.value))
        pyautogui.leftClick()


def pen_set_size(size: int):
    with PenCurrentPosition():
        pyautogui.moveTo(x=tools_pen_pos_x(3), y=tools_pen_pos_y(size))
        pyautogui.leftClick()


if __name__ == '__main__':
    ### pen colors dark
    keyboard.add_hotkey('alt+z', lambda: pen_set_color(Color.light), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('alt+v', lambda: pen_set_color(Color.dark), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('alt+6', lambda: pen_set_color(Color.black), suppress=True, trigger_on_release=True)
    ### pen colors
    keyboard.add_hotkey('alt+1', lambda: pen_set_color(Color.red), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('alt+2', lambda: pen_set_color(Color.orange), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('alt+3', lambda: pen_set_color(Color.olive), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('alt+4', lambda: pen_set_color(Color.green), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('alt+5', lambda: pen_set_color(Color.blue), suppress=True, trigger_on_release=True)
    ### pen size
    keyboard.add_hotkey('alt+q', lambda: pen_set_size(1), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('alt+w', lambda: pen_set_size(2), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('alt+g', lambda: pen_set_size(3), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('alt+h', lambda: pen_set_size(4), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('alt+c', lambda: pen_set_size(5), suppress=True, trigger_on_release=True)
    ### line color
    keyboard.add_hotkey('alt+b', lambda: line_set_color(Color.red), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('alt+a', lambda: line_set_color(Color.orange), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('alt+l', lambda: line_set_color(Color.olive), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('alt+r', lambda: line_set_color(Color.green), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('alt+t', lambda: line_set_color(Color.blue), suppress=True, trigger_on_release=True)


    ### waiting for ctrl-c, control c
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        pass

    # clear keys
    keyboard.clear_hotkey('alt+z')
    keyboard.clear_hotkey('alt+v')
    keyboard.clear_hotkey('alt+6')
    keyboard.clear_hotkey('alt+1')
    keyboard.clear_hotkey('alt+2')
    keyboard.clear_hotkey('alt+3')
    keyboard.clear_hotkey('alt+4')
    keyboard.clear_hotkey('alt+5')
    keyboard.clear_hotkey('alt+q')
    keyboard.clear_hotkey('alt+w')
    keyboard.clear_hotkey('alt+g')
    keyboard.clear_hotkey('alt+h')
    keyboard.clear_hotkey('alt+c')
    keyboard.clear_hotkey('alt+b')
    keyboard.clear_hotkey('alt+a')
    keyboard.clear_hotkey('alt+l')
    keyboard.clear_hotkey('alt+t')
    keyboard.clear_hotkey('alt+r')
