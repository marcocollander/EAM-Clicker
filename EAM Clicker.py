import pyautogui as auto
from PIL import Image
import numpy as np
import time
from pynput import keyboard
import cv2
from sys import stdout
import os
import ctypes


## Global variables
stop_loop = False
abort = False
windowsScaling = 1 # ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100      # opencv is dpi sensitive
scrollVPixels = 0
target_completed = None
target_yes = None
target_employee = None
target_processing = None
target_checkbox_checked = None
target_prompt_icon = None
scale = 0
language = ''
login = ''
action = ''
hours_worked = 1.0
wait_after_processing = True
maxScrolls = 1
 
### KEYBOARD INTERRUPT
def on_press(key):
    global stop_loop
    if key == keyboard.Key.esc:
        print('Escape pressed!')
        stop_loop = True
        #listener.stop()
        #os._exit(1)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

### DETECTING SCALE
def detect_scale():
    print("Detecting scale...")
    scale = 0
    try:
        target_amazonrme = Image.open(resource_path('target_amazonrme.png'))
    except:
        auto.alert(text='Missing target_amazonrme.png', title='EAM Checklist Clicker', button='OK')
        os._exit(0)

    for i in range(100, 74, -5):
        w, h = target_amazonrme.size
        w = int(w*i/100)
        h = int(h*i/100)
        
        if auto.locateOnScreen(target_amazonrme.resize((w,h)), confidence = 0.95, grayscale = True) != None:
            scale = i/100
            break

    if scale == 0:
        for i in range(100, 126, 5):
            w, h = target_amazonrme.size
            w = int(w*i/100)
            h = int(h*i/100)
            if auto.locateOnScreen(target_amazonrme.resize((w,h)), confidence = 0.95, grayscale = True) != None:
                scale = i/100
                break

    if scale > 0:
        print('Closest scale found: ', i, '%')
    else:
        scale = int(auto.prompt(text='Cannot detect browser scaling. Enter manually (i.e. 100):', title='EAM Clicker', default = 0))/100
        if scale != None:
            return scale
        else:            
            os._exit(0)

    return scale

### DETECTING LANGUAGE
def detect_language():
    print("Detecting language...")
    languages = ['en', 'pl', 'de']
    global target_yes
    global target_completed
    global target_employee
    for lang in languages:
        print('Trying ' + str(lang))
        try:
            target_completed = Image.open(resource_path('target_completed_'+lang+'.png'))
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
            
        try:
            target_employee = Image.open(resource_path('target_employee_'+lang+'.png'))
            target_employee = target_employee.resize((int(target_employee.width*scale*windowsScaling),int(target_employee.height*scale*windowsScaling)))
        except:
            auto.alert(text='Missing target_employee_'+lang+'.png', title='EAM Book Labor Clicker', button='OK')
            # os._exit(0)
        
        if auto.locateOnScreen(target_yes, confidence = 0.9, grayscale = True) != None or auto.locateOnScreen(target_completed, confidence = 0.9, grayscale = True) != None or auto.locateOnScreen(target_employee, confidence = 0.9, grayscale = True) != None:
            print('Language detected: ', lang)
            return lang

    lang = auto.confirm(text='Select language?', title='EAM Clicker', buttons=['en', 'pl', 'de'])
    
    try:
        target_completed = Image.open(resource_path('target_completed_'+lang+'.png'))
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
        
    try:
        target_employee = Image.open(resource_path('target_employee_'+lang+'.png'))
        target_employee = target_employee.resize((int(target_employee.width*scale*windowsScaling),int(target_employee.height*scale*windowsScaling)))
    except:
        auto.alert(text='Missing target_employee_'+lang+'.png', title='EAM Book Labor Clicker', button='OK')
        # os._exit(0)
        
    return lang


### WAIT FOR PROCESSING

def wait_for_processing(forceWaitProcessing = False, forceWaitCheckboxes = False, waitForProcessing = True, waitLoopCount = 5, waitForPrompt = False):
    global target_processing
    global target_checkbox_checked
    global target_prompt_icon
    global target_completed
    global target_yes
    global wait_after_processing

    waited = False

    if target_processing == None:
        try:
            target_processing = Image.open(resource_path('target_processing.png'))
            target_processing = target_processing.resize((int(target_processing.width*scale*windowsScaling),int(target_processing.height*scale*windowsScaling)))
        except:
            auto.alert(text='Missing target_processing.png', title='EAM Checklist Clicker', button='OK')
            os._exit(0)
            
    if target_checkbox_checked == None:   
        try:
            target_checkbox_checked = Image.open(resource_path('target_checkbox_checked.png'))
            target_checkbox_checked = target_checkbox_checked.resize((int(target_checkbox_checked.width*scale*windowsScaling),int(target_checkbox_checked.height*scale*windowsScaling)))
        except:
            auto.alert(text='Missing target_checkbox_checked.png', title='EAM Checklist Clicker', button='OK')
            os._exit(0)

    if target_prompt_icon == None:   
        try:
            target_prompt_icon = Image.open(resource_path('target_prompt_icon.png'))
            target_prompt_icon = target_prompt_icon.resize((int(target_prompt_icon.width*scale*windowsScaling),int(target_prompt_icon.height*scale*windowsScaling)))
        except:
            auto.alert(text='Missing target_prompt_icon.png', title='EAM Checklist Clicker', button='OK')
            os._exit(0)


    if waitLoopCount > 0 and forceWaitProcessing:
        print('Forced waiting for processing ', end='')
        stdout.flush()
        j = 0
        while j < waitLoopCount and not stop_loop:
            j += 1
            if auto.locateOnScreen(target_processing, confidence = 0.9, grayscale = True) != None:
                print('!', end='')
                stdout.flush()
                break
            else:
                time.sleep(0.05)
                print('.', end='')
                stdout.flush()
        print('')

    
    # wait for EAM processing / throbler to disappear
    #time.sleep(0.5)
    if waitForProcessing == True or auto.locateOnScreen(target_processing, confidence = 0.9, grayscale = True) != None:
        print('Waiting for EAM ', end='')
        stdout.flush()
        i = 0
        while i < 3 and not stop_loop:
            time.sleep(0.1)
            if auto.locateOnScreen(target_processing, confidence = 0.9, grayscale = True) != None:
                print('.', end='')
                stdout.flush()
                i = 0
                waited = True
            else:
                print('!', end='')
                stdout.flush()
                i += 1
        print('')
        time.sleep(0.3)

    # wait for checkboxes to appear (EAM sucks)

    if waitLoopCount > 0 and forceWaitCheckboxes:
        print('Waiting for checkboxes to appear ', end='')
        stdout.flush()
        i = 0
        j = 0
        while (j < waitLoopCount or i < 3) and not stop_loop:
            j += 1
            #time.sleep(0.05)
            if auto.locateOnScreen(target_completed, confidence = 0.9, grayscale = True) != None or auto.locateOnScreen(target_yes, confidence = 0.9, grayscale = True) != None or auto.locateOnScreen(target_checkbox_checked, confidence = 0.9, grayscale = True) != None:
                i += 1
                print('!', end='')
                stdout.flush()
            else:
                i = 0
                print('.', end='')
                stdout.flush()
        print('')

    # wait for prompt
    #time.sleep(0.5)
    if waitForPrompt == True:
        print('Waiting for prompt ', end='')
        stdout.flush()
        j = 0
        while j < waitLoopCount and not stop_loop:
            time.sleep(0.1)
            j += 1
            if auto.locateOnScreen(target_prompt_icon, confidence = 0.9, grayscale = True) == None:
                print('.', end='')
                stdout.flush()
            else:
                print('!')
                time.sleep(0.1)
                auto.press('space')
                break
        print('')
    
    time.sleep(0.2)

    return waited
        

#################
### MAIN LOOP ###
#################
while scale == 0 or language == '':
    if scale == 0:
        scale = detect_scale()
        scrollVPixels = int(- 800 / scale / windowsScaling / (1920 / ctypes.windll.user32.GetSystemMetrics(0)))
    if language == '':
        language = detect_language()

# keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()
    
while action != 'Exit' and action != None:

    stop_loop = False
    action = auto.confirm(text='Select action:', title='EAM Clicker', buttons=['Complete Checklist', 'Fill Book Labor', 'Exit'])
   

# \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/

    ##############################
    ### CHECKLIST CLICKER LOOP ###
    ##############################
    if action == 'Complete Checklist':

        auto.alert(text='To stop action press ESCAPE.', title='EAM Checklist Clicker')
        retry = 0
        scroll = 0
        click_counter = 0

        print('Starting')
        loop_break = False
        while not stop_loop:

                            
            # click everything on screen
            time.sleep(0.1)
            target_list = list(auto.locateAllOnScreen(target_completed, confidence = 0.9, grayscale = True))
            target_list += list(auto.locateAllOnScreen(target_yes, confidence = 0.9, grayscale = True))

            if target_list and not stop_loop:
                for i in target_list:
                    auto.click(auto.center(i))
                    click_counter += 1
                        
                    scroll = 0
                    retry = 0
            
            # if nothing else to click, scroll down
            elif not stop_loop:
                # proceed to next WO
                if scroll == maxScrolls:
                    print('Next please')
                    auto.hotkey('ctrl', 'down')
                    if wait_for_processing(waitForProcessing = True, waitLoopCount = 30):
                        scroll = 0
                        retry = 0
                    #time.sleep(1)
                    retry += 1
                    scroll = 0
                    
                else:
                    print('Scroll (', int(scroll + 1), ')')
                    auto.scroll(scrollVPixels)
                    if wait_for_processing(waitForProcessing = True):
                        scroll = 0
                        retry = 0
                    #auto.hotkey('pgdown')
                    #time.sleep(0.15)
                    scroll += 1

                # if proceeding does not prompt EAM processing, save last WO and exit program
                if retry > 2:
                    auto.hotkey('ctrl', 's')
                    print('Done!')
                    auto.alert(text='Clicked ' + str(click_counter) + ' times. No more checkboxes found. Closing.', title='EAM Checklist Clicker', button='OK')
                    break
            

# /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\




# \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/

    #######################
    ### BOOK LABOR LOOP ###
    #######################
    elif action == 'Fill Book Labor':
            
            # prompt for login / default windows username
            login = auto.prompt(text='Login', title='EAM Book Labor Clicker', default=str(os.getlogin()).upper())
            if login == None:
                stop_loop = True

            # ask for hours type
            hours_type = auto.confirm(text='Normal or overtime hours?', title='EAM Book Labor Clicker', buttons=['Normal', 'Overtime'])[0]
            if hours_type == None:
                stop_loop = True

            # ask for date
            date = auto.confirm(text='Date worked?', title='EAM Book Labor Clicker', buttons=['Today', 'Other'])[0]
            if date == 'O':
                while True and date != None:
                    date = auto.prompt(text='Date in EAM format (i.e. 16-MAY-2022):', title='EAM Book Labor Clicker', default='')
                    try:
                        x = date.split('-')
                        if int(x[0]) <= 31 and int(x[0]) > 0 and x[1].isalpha() and len(x[1]) == 3 and int(x[2]) > 2000 and int(x[2]) < 3000:
                            break
                    except:
                        auto.alert(text='Wrong date format! Use EAM formatting i.e. 17-MAY-2022, 17-MAJ-2022 etc.', title='EAM Book Labor Clicker', button='OK')
                        pass
            elif date == None:
                stop_loop = True


            last_hours_worked_input = '0'
        
            # start loop
            while login != None and hours_type != None and date != None and not stop_loop:
                hours_worked = auto.confirm(text='How many hours?', title='EAM Book Labor Clicker', buttons=['0.1', '0.25', '0.33', '0.5', '0.75', '1', '1.5', '2', 'Other', 'Exit'])
                if hours_worked == 'Other':
                    hours_worked = auto.prompt(text='Enter hours worked', title='EAM Book Labor Clicker', default=last_hours_worked_input)
                    last_hours_worked_input = hours_worked
                    if not (float(hours_worked) > 0 and float(hours_worked) <= 11.5) or hours_worked == None:
                        if hours_worked != None:
                            auto.alert(text='Bad input! Hours must be 0 < h <= 11.5 !', title='EAM Book Labor Clicker', button='OK')
                        break
                        
                elif hours_worked == 'Exit' or hours_worked == None:
                    break

                # Click on employee and type in login
                i = 0
                while i < 5:
                    i += 1
                    target_location = auto.locateOnScreen(target_employee, confidence = 0.9, grayscale = True)
                    if target_location != None:
                        break
                try:
                    auto.click(target_location)
                    auto.write(login)
                except:
                    auto.alert(text='Cannot find EMPTY Employee field!', title='EAM Book Labor Clicker', button='OK')
                    break
                    

                # Jumpt to Crew / Departament
                auto.press('tab')
                #time.sleep(0.25)
                wait_for_processing(forceWaitProcessing = True, waitLoopCount = 5)

                # Jump to Trade
                auto.press('tab')
                #time.sleep(0.1)

                # Jumpt to Date
                auto.press('tab')
                #time.sleep(0.1)
                
                # Clear Date
                auto.press('backspace')
                #time.sleep(0.25)

                # Enter new date
                if date == 'T':
                    auto.press('space')
                    #wait_for_processing(waitForProcessing = True)
                else:
                    auto.write(str(date))
                    
                # Jump to Type of Hours
                
                wait_for_processing(waitForProcessing = True)
            
                auto.press('tab')
                wait_for_processing(forceWaitProcessing = False, waitLoopCount = 5, waitForProcessing = False, waitForPrompt = True)
            

                # Type in hours type
                if hours_type != 'N':
                    auto.write(hours_type)

                # Remove this part if COVID field has been removed
                # \/ \/ \/ \/ \/ \/
                auto.press('tab')
                # /\ /\ /\ /\ /\ /\

                # Wait for process only if Type of Hours field has been changed
                if hours_type != 'N':
                    wait_for_processing(waitForProcessing = True)

                # Jump to Hours Worked
                auto.press('tab')

                #time.sleep(0.1)
                auto.write(str(hours_worked))
                #time.sleep(0.25)

                # Save
                auto.press('enter')
                wait_for_processing(waitForProcessing = True)
                time.sleep(1)

# /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\ /\


try:
    listener.stop()  
except:
    pass

os._exit(0)
