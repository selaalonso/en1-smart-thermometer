from thermocouple import MAX31855
from s2pico_oled import OLED
from machine import Pin, I2C
from time import sleep 

# set up the thermocouple, oled display, and buttons 
therm = MAX31855(cs=Pin(13), sck=Pin(17), so=Pin(35))
oled = OLED(i2c, Pin(18))
bread_button = Pin(1, Pin.IN, Pin.PULL_UP)
muffin_button = Pin(2, Pin.IN, Pin.PULL_UP)
roll_button = Pin(3, Pin.IN, Pin.PULL_UP)
stop_button = Pin(4, Pin.IN, Pin.PULL_UP) 

temp_range = list()
treat = "" 

# assign temp range and treat type based on button pressed 
def buttonPressed():
    if bread_button == 0:
        temp_range = {195, 200}
        treat = "bread" 
    elif muffin_button == 0:
        temp_range = {200, 205}
        treat = "muffins" 
    elif roll_button == 0:
        temp_range = {185, 190}
        treat = "rolls" 
    else:
        return false
    return true

while not buttonPressed(): # wait for setting to be chosen 
    buttonPressed()

# display message on screen for 3 seconds showing the user's choice 
oled.fill(0)
oled.text(f"You chose: {treat}", 3, 10, 1)
sleep(3) 

while stop_button == 1:
    # the treat isn't done baking if the temp is less than the range minimum 
    if therm.read() < temp_range[0]:  
        oled.fill(0)
        oled.text(f"current temp: {therm.read()}", 3, 10, 1)
        oled.text(f"desired temp: {temp_range[0]}-{temp_range[1]}˚C", 3, 20, 1) 
        oled.show()
    # the treat is done baking if the temp is within the desired range 
    else if therm.read() >= temp_range[0] and therm.read() <= temp_range[1]: 
        oled.fill(0)
        if treat == "bread":
            oled.text("your bread is ready!", 3, 10, 1)
        else:
            oled.text(f"your {treat} are ready!", 3, 10, 1)
        oled.show()
    # the treat is burning if the temp is above the range maximum 
    else: 
        oled.fill(0)
        if treat == "bread":
            oled.text("your bread is burning!", 3, 10, 1)
        else:
            oled.text(f"your {treat} are burning!", 3, 10, 1)
        oled.show()
    sleep(2) 

# reset screen to blank 
oled.fill(0)
oled.show() 