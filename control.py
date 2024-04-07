from file_manager import save_date
from machine import Pin
import uasyncio
import utime

class Relay():
    def __init__(self, pin):
        self.switch = Pin(pin, Pin.OUT)
    
    def on(self):
        self.switch.value(1)
        save_date()
        
    def off(self):
        self.switch.value(0)        
    
    async def on_off(self):
        self.on()
        await uasyncio.sleep_ms(200)
        self.off()
        
    async def reset(self):
        self.on()
        await uasyncio.sleep_ms(5000)
        self.off()
        print('Resetting PC')

    
class LedStatus():
    def __init__(self):
        self.led = Pin(2, Pin.OUT)
    
    def on(self):
        self.led.on()    
    
    def off(self):
        self.led.off()
        
    def turn_on(self, n):
        self.led.on()
        utime.sleep(n)     
        self.led.off()
    
