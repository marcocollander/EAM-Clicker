import pyautogui as auto
from PIL import Image
import numpy as np
#import imutils
import time
from pynput import keyboard
import cv2
from sys import stdout
import os
import tkinter as tk
import ctypes


 
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

## DETERMINING SCALE
# load targets
print("Detecting scale...")
try:
    target_amazonrme = Image.open(resource_path('target_amazonrme.png'))
except:
    print('Missing target_amazonrme.png')
    abort = True


if abort:
    print('Missing target file(s). Aborting.')
    time.sleep(5)
    os._exit(0)

scale = 0
windowsScaling = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

for i in range(100, 49, -1):
    w, h = target_amazonrme.size
    w = int(w*i/100)
    h = int(h*i/100)
    if auto.locateOnScreen(target_amazonrme.resize((w,h)), confidence = 0.95, grayscale = True) != None:
        scale = i/100
        break

if scale == 0:
    for i in range(100, 151, 1):
        w, h = target_amazonrme.size
        w = int(w*i/100)
        h = int(h*i/100)
        if auto.locateOnScreen(target_amazonrme.resize((w,h)), confidence = 0.95, grayscale = True) != None:
            scale = i/100
            break

if scale > 0:
    print('Closest scale found: ', i, '%')

scrollCount = int(-700 / scale / windowsScaling / (1920 / ctypes.windll.user32.GetSystemMetrics(0)))
## DETERMINING LANGUAGE
print("Detecting language...")
languages = ['en', 'pl', 'de']
abort = True
for language in languages:
    try:
        target_completed = Image.open(resource_path('target_completed_'+language+'.png'))
        target_completed = target_completed.resize((int(target_completed.width*scale*windowsScaling),int(target_completed.height*scale*windowsScaling)))
    except:
        print('Missing target_completed_'+language+'.png')
        abort = True
    try:
        target_yes = Image.open(resource_path('target_yes_'+language+'.png'))
        target_yes = target_yes.resize((int(target_yes.width*scale*windowsScaling),int(target_yes.height*scale*windowsScaling)))
    except:
        print('Missing target_yes_'+language+'.png')
        abort = True
    if auto.locateOnScreen(target_yes, confidence = 0.8, grayscale = True) != None or auto.locateOnScreen(target_completed, confidence = 0.8, grayscale = True) != None:
        print('Language detected: ', language)
        abort = False
        break

if abort:
    print('Language not detected. Please open Checklist tab. Aborting.')
    time.sleep(5)
    os._exit(0)
    
try:
    target_processing = Image.open(resource_path('target_processing.png'))
    target_processing = target_processing.resize((int(target_processing.width*scale*windowsScaling),int(target_processing.height*scale*windowsScaling)))
except:
    print('Missing target_processing.png')
    abort = True
    
try:
    target_checkbox_checked = Image.open(resource_path('target_checkbox_checked.png'))
    target_checkbox_checked = target_checkbox_checked.resize((int(target_checkbox_checked.width*scale*windowsScaling),int(target_checkbox_checked.height*scale*windowsScaling)))
    #print((int(target_checkbox_checked.width*scale*windowsScaling),int(target_checkbox_checked.height*scale*windowsScaling)))
except:
    print('Missing target_checkbox_checked.png')
    abort = True
  

# keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

time.sleep(1)
retry = 0
scroll = 0
wait_after_processing = False


window = tk.Tk()
frame = tk.Frame()
frame.pack()

#window.mainloop()



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
            if auto.locateOnScreen(target_completed, confidence = 0.8, grayscale = True) != None or auto.locateOnScreen(target_yes, confidence = 0.8, grayscale = True) != None or auto.locateOnScreen(target_checkbox_checked, confidence = 0.8, grayscale = True) != None:
                time.sleep(0.05)
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
    target_list = list(auto.locateAllOnScreen(target_completed, confidence = 0.8, grayscale = True))
    target_list += list(auto.locateAllOnScreen(target_yes, confidence = 0.8, grayscale = True))

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
            auto.scroll(scrollCount)
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


