import os
import sys
import ctypes
import numpy as np
import pyautogui
import time
import pydirectinput
import threading
import traceback
from pynput import keyboard
from skimage.metrics import structural_similarity as ssim

fishing_image_np = None # 낚시중
hooking_image_np = None # 후킹중
miss_image_np = None # 실패

begin = False

def on_press(key):
    global fishing_image_np, hooking_image_np, miss_image_np, begin
    try:
        if keyboard.Key.f1 == key:
            fishing_image = pyautogui.screenshot(region=(790,260, 25, 40))
            fishing_image_np = np.array(fishing_image)
            print("F1: Fishing Image")
        elif keyboard.Key.f2 == key:
            hooking_image = pyautogui.screenshot(region=(670,320, 25, 60))
            hooking_image_np = np.array(hooking_image)
            print("F2: Hooking Image")
        elif keyboard.Key.f3 == key:
            miss_image = pyautogui.screenshot(region=(860, 350, 60, 20))
            miss_image_np = np.array(miss_image)
            print("F3: Miss Image")
        elif keyboard.Key.f4 == key:
            begin = not begin
    except Exception:
        traceback.print_exc()

listener_thread = threading.Thread(target=lambda: keyboard.Listener(on_press=on_press).start())
listener_thread.daemon = True
listener_thread.start()

error_detect_count = 0

def fishing():
    global error_detect_count
    try:
        global fishing_image_np, hooking_image_np, miss_image_np
        fishing_image = pyautogui.screenshot(region=(790, 260, 25, 40))
        fishing_test_image_np = np.array(fishing_image)
        similarity = ssim(fishing_image_np, fishing_test_image_np, multichannel=True, win_size=3)
        if similarity > 0.6:
            error_detect_count = 0
        else:
            error_detect_count += 1
        if error_detect_count > 30:
            error_detect_count = 0
            pydirectinput.press('F6')
    except:
        pass

    try:
        hooking_image = pyautogui.screenshot(region=(670, 320, 25, 60))
        hooking_test_image_np = np.array(hooking_image)
        similarity = ssim(hooking_image_np, hooking_test_image_np, multichannel=True, win_size=3)
        if similarity > 0.7:
            pydirectinput.press('F5') # click
            pydirectinput.press('F6') # ctrl
    except:
        pass

    try:
        miss_image = pyautogui.screenshot(region=(860, 350, 60, 20))
        miss_test_image_np = np.array(miss_image)
        similarity = ssim(miss_image_np, miss_test_image_np, multichannel=True, win_size=3)
        if similarity > 0.5:
            pydirectinput.press('F6') # ctrl
    except:
        pass


def fishing_loop():
    while True:
        time.sleep(0.2)
        if begin:
            fishing()

fishing_thread = threading.Thread(target=fishing_loop)
fishing_thread.daemon = True
fishing_thread.start()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("관리자 권한으로 실행 중입니다. 프로그램을 다시 시작합니다...")
    ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, ' '.join(sys.argv), None, 1)
    sys.exit()

ctypes.windll.shell32.ShellExecuteW(None, 'runas', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys.exe'), None, None, 1)

print("낚시시작 F1, 후킹중 F2, Miss M3, 시작/정지 F4")
while True:
    time.sleep(1)