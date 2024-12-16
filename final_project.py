from thermocouple import MAX31855
from s2pico_oled import OLED
from machine import Pin, I2C
import time
from time import sleep 

# set up the thermocouple, oled display, and buttons 
therm = MAX31855(cs=Pin(13), sck=Pin(17), so=Pin(35))
oled = OLED(i2c, Pin(18))
bread_button = Pin(1, Pin.IN, Pin.PULL_UP)
muffin_button = Pin(3, Pin.IN, Pin.PULL_UP)
roll_button = Pin(5, Pin.IN, Pin.PULL_UP)
stop_button = Pin(6, Pin.IN, Pin.PULL_UP) 

temp_range = list()
treat = ""

continue_loop = True 
while continue_loop: # wait for setting to be chosen 
    # buttonPressed()
    if bread_button.value() == 0:
        temp_range = [90, 93]
        treat = "bread"
        continue_loop = False 
    elif muffin_button.value() == 0:
        temp_range = [93, 96]
        treat = "muffins"
        continue_loop = False 
    elif roll_button.value() == 0:
        temp_range = [85, 88]
        treat = "rolls"
        continue_loop = False 
    

# display message on screen for 3 seconds showing the user's choice 
oled.fill(0)
oled.text(f"You chose: ", 3, 10, 1)
oled.text(f"{treat}", 3, 20, 1)
oled.show()
sleep(3)

current_time = int(time.time())
current_temp = therm.read() 

while stop_button.value() != 0:
    if int(time.time()) > current_time:
        current_time = int(time.time())
        current_temp = int(therm.read())
        print(f"{current_time}, {current_temp}") 
    # the treat isn't done baking if the temp is less than the range minimum
    if current_temp < temp_range[0]:  
        oled.fill(0)
        oled.text(f"current: {current_temp}", 3, 10, 1)
        oled.text(f"goal: {temp_range[0]}-{temp_range[1]}", 3, 20, 1) 
        oled.show()
    # the treat is done baking if the temp is within the desired range 
    elif current_temp >= temp_range[0] and current_temp <= temp_range[1]: 
        oled.fill(0)
        oled.text("ready!", 3, 10, 1) 
        oled.show()
    # the treat is burning if the temp is above the range maximum 
    else: 
        oled.fill(0)
        oled.text("burning!", 3, 10, 1) 
        oled.show()

# reset screen to blank 
oled.fill(0)
oled.show() 