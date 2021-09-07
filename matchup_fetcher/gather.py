import json
import time

# This is needed for pyautogui
import os
os.environ['DISPLAY'] = ':0'

import keyboard
import pyautogui

with open("controls.json", 'r') as f:
    controls = json.load(f)

count = 0
while (count < 5):
    time.sleep(1/60)

    keyboard.write(controls['down'], delay=0)
    keyboard.write(controls['show_results'], delay=0)
    screen_shot = pyautogui.screenshot()
    screen_shot.save('attempt_%s.png' % count)
    count += 0
