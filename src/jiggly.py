import pyautogui
import threading
from pynput import mouse
import random
import time
import yaml
from framework.Argv import Argv

JIGGLE_INTERVAL = float(Argv.get('interval',1.2))  # seconds
JIGGLE_RADIUS = int(Argv.get('radius',100))  # pixels
JIGGLE_IDLE_TIME = int(Argv.get('idle',2))
BUS = Argv.get('bus','no bus')


JIGGLE_RUNNING = False
LAST_MOVE_TIME = time.time()

def start_jiggle():
    global JIGGLE_RUNNING
    JIGGLE_RUNNING = True
    start_pos = pyautogui.position()
    while JIGGLE_RUNNING:
        check_for_quit()
        x_offset, y_offset = random.randint(-JIGGLE_RADIUS, JIGGLE_RADIUS), random.randint(-JIGGLE_RADIUS, JIGGLE_RADIUS)
        new_pos = start_pos[0] + x_offset, start_pos[1] + y_offset
        new_pos = pyautogui.Point(min(start_pos[0] + JIGGLE_RADIUS, max(start_pos[0] - JIGGLE_RADIUS, new_pos[0])),
                                   min(start_pos[1] + JIGGLE_RADIUS, max(start_pos[1] - JIGGLE_RADIUS, new_pos[1])))
        pyautogui.moveTo(new_pos, duration=JIGGLE_INTERVAL)

def stop_jiggle():
    global JIGGLE_RUNNING
    JIGGLE_RUNNING = False

def on_move(x, y):
    global LAST_MOVE_TIME
    if JIGGLE_RUNNING and x != pyautogui.position().x and y != pyautogui.position().y:
        stop_jiggle()
    LAST_MOVE_TIME = time.time()

def check_for_quit():
    with open(BUS,'r') as editor_file:
        editor = yaml.safe_load(editor_file)
        isActive = editor['active']
        if isActive is False:
            quit()

def quit():
    global listener
    listener.stop()
    exit()

def check_activity():
    global LAST_MOVE_TIME
    global JIGGLE_IDLE_TIME
    while True:
        check_for_quit()
        time_since_last_move = time.time() - LAST_MOVE_TIME
        if not JIGGLE_RUNNING and time_since_last_move > JIGGLE_IDLE_TIME:
            start_jiggle()
        time.sleep(1)


with mouse.Listener(on_move=on_move) as listener:
    t = threading.Thread(target=check_activity)
    t.start()
    LAST_MOVE_TIME = time.time()
    listener.join()
