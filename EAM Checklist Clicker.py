import pyautogui as auto
from PIL import Image
import numpy as np
#import imutils
import time
from pynput import keyboard
import cv2
from sys import stdout
import os
#import tkinter as tk
import ctypes

loop_break = False
abort = False
windowsScaling = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
scrollCount = 0
target_completed = None
target_yes = None
target_employee = None
scale = 0
language = ''
login = ''
action = ''
hours_worked = 1.0
 
### KEYBOARD INTERRUPT
def on_press(key):
    if key == keyboard.Key.esc:
        print('Stopping')
        listener.stop()
        os._exit(1)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

### DETECTING SCALE
def detect_scale():
    print("Detecting scale...")
    global scrollCount
    scale = 0
    try:
        target_amazonrme = Image.open(resource_path('target_amazonrme.png'))
    except:
        auto.alert(text='Missing target_amazonrme.png', title='EAM Checklist Clicker', button='OK')
        os._exit(0)

    for i in range(100, 74, -1):
        w, h = target_amazonrme.size
        w = int(w*i/100)
        h = int(h*i/100)
        if auto.locateOnScreen(target_amazonrme.resize((w,h)), confidence = 0.95, grayscale = True) != None:
            scale = i/100
            break

    if scale == 0:
        for i in range(100, 126, 1):
            w, h = target_amazonrme.size
            w = int(w*i/100)
            h = int(h*i/100)
            if auto.locateOnScreen(target_amazonrme.resize((w,h)), confidence = 0.95, grayscale = True) != None:
                scale = i/100
                break

    if scale > 0:
        print('Closest scale found: ', i, '%')
    else:
        auto.alert(text='Cannot detect scale. Open Checklist tab with visible Result column.', title='EAM Checklist Clicker', button='OK')
        os._exit(0)

    scrollCount = int(-700 / scale / windowsScaling / (1920 / ctypes.windll.user32.GetSystemMetrics(0)))
    return scale

### DETECTING LANGUAGE
def detect_language():
    print("Detecting language...")
    languages = ['en', 'pl', 'de']
    global target_yes
    global target_completed
    abort = True
    for lang in languages:
        try:
            target_completed = Image.open(resource_path('target_completed_'+lang+'.png'))
            print('target_completed_'+lang+'.png')
            target_completed = target_completed.resize((int(target_completed.width*scale*windowsScaling),int(target_completed.height*scale*windowsScaling)))
        except:
            auto.alert(text='Missing target_completed_'+lang+'.png', title='EAM Checklist Clicker', button='OK')
            os._exit(0)
        try:
            target_yes = Image.open(resource_path('target_yes_'+lang+'.png'))
            target_yes = target_yes.resize((int(target_yes.width*scale*windowsScaling),int(target_yes.height*scale*windowsScaling)))
        except:
            auto.alert(text='Missing target_yes_'+lang+'.png', title='EAM Checklist Clicker', button='OK')
            os._exit(0)
        if auto.locateOnScreen(target_yes, confidence = 0.8, grayscale = True) != None or auto.locateOnScreen(target_completed, confidence = 0.8, grayscale = True) != None:
            print('Language detected: ', lang)
            language = lang
            abort = False
            break

    if abort:
        auto.alert(text='Cannot detect language. Make sure checklist is visible.', title='EAM Checklist Clicker', button='OK')
        os._exit(0)

    return lang

### DETECTING LANGUAGE FOR BOOK LABOR TAB
def detect_language_BL():
    print("Detecting language...")
    languages = ['en', 'pl', 'de']
    global target_employee
    abort = True
    for lang in languages:
        try:
            target_employee = Image.open(resource_path('target_employee_'+lang+'.png'))
            print('target_employee_'+lang+'.png')
            target_employee = target_employee.resize((int(target_employee.width*scale*windowsScaling),int(target_employee.height*scale*windowsScaling)))
        except:
            auto.alert(text='Missing target_employee_'+lang+'.png', title='EAM Book Labor Clicker', button='OK')
            os._exit(0)
        if auto.locateOnScreen(target_employee, confidence = 0.8, grayscale = True) != None:
            print('Language detected: ', lang)
            language = lang
            abort = False
            break

    if abort:
        auto.alert(text='Cannot detect language. Make sure Book Labor tab is opened and visible.', title='EAM Book Labor Clicker', button='OK')
        os._exit(0)

    return lang



#################
### MAIN LOOP ###
#################

while action != 'Exit':
    action = auto.confirm(text='Starting. To exit press ESCAPE any time.', title='EAM Checklist Clicker', buttons=['Complete Checklist', 'Fill Book Labor', 'Exit'])

# \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/

    ##############################
    ### CHECKLIST CLICKER LOOP ###
    ##############################
    if action == 'Complete Checklist':

        if scale == 0:
            scale = detect_scale()

        if language == '':
            language = detect_language()
            
        try:
            target_processing = Image.open(resource_path('target_processing.png'))
            target_processing = target_processing.resize((int(target_processing.width*scale*windowsScaling),int(target_processing.height*scale*windowsScaling)))
        except:
            auto.alert(text='Missing target_processing.png', title='EAM Checklist Clicker', button='OK')
            os._exit(0)
            
        try:
            target_checkbox_checked = Image.open(resource_path('target_checkbox_checked.png'))
            target_checkbox_checked = target_checkbox_checked.resize((int(target_checkbox_checked.width*scale*windowsScaling),int(target_checkbox_checked.height*scale*windowsScaling)))
            #print((int(target_checkbox_checked.width*scale*windowsScaling),int(target_checkbox_checked.height*scale*windowsScaling)))
        except:
            auto.alert(text='Missing target_checkbox_checked.png', title='EAM Checklist Clicker', button='OK')
            os._exit(0)
          

        # keyboard listener
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        time.sleep(1)
        retry = 0
        scroll = 0
        wait_after_processing = False

        print('Starting')
        loop_break = False
        while not loop_break:

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
                time.sleep(0.3)

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
                    if i == 29:
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
                if retry > 2:
                    auto.hotkey('ctrl', 's')
                    print('Done!')
                    auto.alert(text='No more checkboxes found. Closing.', title='EAM Checklist Clicker', button='OK')
                    listener.stop()
                    break

# /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\




# \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/

    #######################
    ### BOOK LABOR LOOP ###
    #######################
    if action == 'Fill Book Labor':
        if login == '':
            login = auto.prompt(text='Login', title='EAM Book Labor Clicker', default='')

        hour_type = auto.confirm(text='Normal or overtime hours?', title='EAM Checklist Clicker', buttons=['Normal', 'Overtime'])[0]
        
        if scale == 0:
            scale = detect_scale()

        if language == '':
            language = detect_language_BL()

        auto.click(auto.locateOnScreen(target_employee, confidence = 0.8, grayscale = True))
        auto.write(login, interval=0.05)
        auto.press('tab')
        time.sleep(1)
        auto.press('tab')
        time.sleep(1)
        auto.press('tab')
        time.sleep(1)
        auto.press('space')
        time.sleep(1)
        auto.press('tab')
        time.sleep(3)
        if hour_type != 'N':
            auto.write(hour_type)
            time.sleep(3)
        auto.press('tab')
        time.sleep(1)
        auto.write(str(hours_worked))

# /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\


try:
    listener.stop()  
except:
    pass

os._exit(0)
