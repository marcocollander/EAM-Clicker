import pyautogui as auto
from PIL import Image
import numpy as np
#import imutils
import time
from pynput import keyboard
import cv2
from sys import stdout
import os

 
# keyboard interupt
def on_press(key):
    if key == keyboard.Key.esc:
        print('Stopping')
        listener.stop()
        os._exit(0)

abort = False

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# load targets
try:
    target_completed = Image.open(resource_path('target_completed.png'))
except:
    print('Missing target_completed.png')
    abort = True
try:
    target_yes = Image.open(resource_path('target_yes.png'))
except:
    print('Missing target_yes.png')
    abort = True
try:
    target_processing = Image.open(resource_path('target_processing.png'))
except:
    print('Missing target_processing.png')
    abort = True
    
if abort:
    print('Missing target file(s). Aborting.')
    time.sleep(5)
    os._exit(0)

# keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

time.sleep(1)
retry = 0
scroll = 0
wait_after_processing = False


print('Starting')

while True:

    # wait for EAM processing
    if wait_after_processing == True or auto.locateOnScreen(target_processing, confidence = 0.7) != None:
        print('Waiting for EAM ', end='')
        stdout.flush()
        i = 0
        while i < 3:
            if auto.locateOnScreen(target_processing, confidence = 0.7) != None:
                i = 0
                retry = 0
                scroll = 0
            time.sleep(0.1)
            print('.', end='')
            stdout.flush()
            i += 1
        print('')

        # wait for checkboxes to appear (EAM sucks)
        for i in range(0,30):
            if auto.locateOnScreen(target_completed, confidence = 0.85, grayscale = True) != None or auto.locateOnScreen(target_yes, confidence = 0.85, grayscale = True) != None:
                time.sleep(0.1)
                if i != 0:
                    print('')
                break
            if i == 0:
                print('Waiting for checkboxes ', end='')
            else:
                print('.', end='')
                stdout.flush()
                time.sleep(0.1)
            if i == 9:
                print('')
                
        wait_after_processing = False
        #time.sleep(1)

        
    # click everything on screen
    target_list = list(auto.locateAllOnScreen(target_completed, confidence = 0.85, grayscale = True))
    target_list += list(auto.locateAllOnScreen(target_yes, confidence = 0.85, grayscale = True))

    if target_list:
        for i in target_list:
            auto.click(auto.center(i))
            #print('Click')
                
            time.sleep(0.05)
            scroll = 0
            retry = 0
    # if nothing else to click, scroll down
    else:
        # proceed to next WO
        if scroll == 2 :
            print('Next please')
            auto.hotkey('ctrl', 'down')
            #time.sleep(1)
            retry += 1
            scroll = 0
            wait_after_processing = True
            
        else:
            print('Scroll (', int(scroll + 1), ')')
            auto.scroll(-650)
            #auto.hotkey('pgdown')
            time.sleep(0.15)
            scroll += 1

        # if proceeding does not prompt EAM processing, save last WO and exit program
        if retry > 4:
            auto.hotkey('ctrl', 's')
            print('Done!')
            auto.alert(text='No more checkboxes found. Closing.', title='WO KO', button='OK')
            listener.stop()
            os._exit(0)


