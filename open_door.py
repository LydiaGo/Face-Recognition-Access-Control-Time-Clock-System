from machine import Pin, PWM
from time import sleep

servoPin = PWM(Pin(16))
servoPin.freq(50)

def servo(degrees):
    if degrees > 180:
        degrees = 180
    if degrees < 0:
        degrees = 0
    maxDuty = 8200
    minDuty = 1600
    newDuty = minDuty + (maxDuty-minDuty) * (degrees/180)
    servoPin.duty_u16(int(newDuty))
    
#開門角度調整
while True:
    servoPin.duty_u16(8500)
    sleep(1.5)
    servoPin.duty_u16(4500)
    sleep(1.5)