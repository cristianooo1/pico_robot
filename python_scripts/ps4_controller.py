import sys
import time
import os

sys.path.insert(0, "/home/cristianooo/pico_robot/lib/Gamepad")
import Gamepad

class PS4Controller:
    def __init__(self):

        self.gamepad_type = Gamepad.PS4
        self.poll_interval = 0.1
        self.running = False
        self.pad = self.gamepad_type()
        self.buttons = {
            'ButtonFWD': 'TRIANGLE',
            'ButtonBWD': 'CROSS',
            'ButtonROT_LEFT': 'SQUARE',
            'ButtonROT_RIGHT': 'CIRCLE',
            'ButtonExit': 'PS'
        }
        self.pressed_buttons = set()
        self.linear = 0.0
        self.angular = 0.0
        

    def connect(self):
        if not Gamepad.available():
            print('Please connect your gamepad...')
            while not Gamepad.available():
                time.sleep(1.0)
        # self.pad = self.gamepad_type()
        self.running = True
        self.pad.startBackgroundUpdates()
        print('Gamepad connected')

    def disconnect(self):
        if self.pad:
            self.pad.disconnect()
        self.running = False
        print('Gamepad disconnected')

    def get_states(self):
        states = {}
        for name, button in self.buttons.items():
            if self.pad.isPressed(button):
                states[name] = 'PRESSED'
            elif self.pad.beenReleased(button):
                states[name] = 'RELEASED'
            else:
                states[name] = 'IDLE'
            
        return states
    
    def handlerr(self, states):
        if states['ButtonExit'] == 'PRESSED':
            print('EXIT')
            return False


        if states['ButtonFWD'] == 'PRESSED':
            self.on_button_press('ButtonFWD')
            
        elif states['ButtonFWD'] == 'RELEASED':
            self.on_button_release('ButtonFWD')


        
        if states['ButtonBWD'] == 'PRESSED':
            self.on_button_press('ButtonBWD')
        elif states['ButtonBWD'] == 'RELEASED':
            self.on_button_release('ButtonBWD')


        if states['ButtonROT_LEFT'] == 'PRESSED':
            self.on_button_press('ButtonROT_LEFT')
        elif states['ButtonROT_LEFT'] == 'RELEASED':
            self.on_button_release('ButtonROT_LEFT')
        
        if states['ButtonROT_RIGHT'] == 'PRESSED':
            self.on_button_press('ButtonROT_RIGHT')
        elif states['ButtonROT_RIGHT'] == 'RELEASED':
            self.on_button_release('ButtonROT_RIGHT')

        return True
    
    def on_button_press(self, button):
        before = len(self.pressed_buttons)
        self.pressed_buttons.add(button)
        if len(self.pressed_buttons) != before:
            if (button == 'ButtonFWD'):
                self.linear = 0.10
                print("linear is now 0.10")
            elif (button == 'ButtonBWD'):
                self.linear = -0.10
                print("linear is now -0.10")
            elif (button == 'ButtonROT_LEFT'):
                self.angular = 1.5
                print("angular is now 0.10")
            elif (button == 'ButtonROT_RIGHT'):
                self.angular = -1.5
                print("angular is now -0.10")


    def on_button_release(self, button):
        try:
            self.pressed_buttons.remove(button)
            print("velocity is now 0.0")
            self.linear = 0.0
            self.angular = 0.0
        except KeyError:
            pass
    
    def run_controller_loop(self, handler):
        try:
            if (self.running and self.pad.isConnected()):
                states = self.get_states()
                cond = handler(states)
                if cond is False:
                    self.running = False
                    # sys.exit()
                    # exit()
                
        finally:
            # self.disconnect()
            pass