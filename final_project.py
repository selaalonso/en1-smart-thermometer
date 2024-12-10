from thermocouple import MAX31855
from s2pico_oled import OLED
from machine import Pin, I2C
from time import sleep 

# set up the thermocouple & oled display 
therm = MAX31855(cs=Pin(13), sck=Pin(17), so=Pin(35))
# oled = OLED(i2c, Pin(18))

while True:
    oled.fill(0)
    oled.text(f"temp: {therm.read()}", 3, 10, 1) # print thermocouple reading to oled screen
    oled.show()
    sleep(1) # wait one second before reading another value from the thermocouple 