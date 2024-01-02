import Layout
from machine import Pin, PWM
from time import sleep

class Sensor:
    def __init__(self, pin_number, name):
        self.sensor = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        self.name = name
    
    def read(self):
        return self.sensor.value()

class Point:
    def __init__(self, pins):
        self.status = True #True is UP
        self.up = Pin(pins['UP'], Pin.OUT)
        self.down = Pin(pins['DOWN'], Pin.OUT)
        #Set your initial pin values - True is 1 in python and 0 is false, so we can use boolean logic for these
        self.up.value(True)
        self.down.value(False)
    
    def switch(self):
        #Not 100% sure quite what you were doing with the relays, I think you want one to be true and the other to be false?
        self.up.value(not self.status)
        sleep(0.2)
        self.down.value(self.status)
        self.status = not self.status

class Track:
    def __init__(self, details):
        self.speed = PWM(Pin(details['Speed']))
        self.signal_a = Pin(details['Signal_a'], Pin.OUT)
        self.signal_b = Pin(details['Signal_b'], Pin.OUT)
        self.signal_a.value(False)
        self.signal_b.value(False)
    
    def set_direction(self, direction):
        #Use True for up and False for down
        self.signal_a.value(direction)
        self.signal_b.value(not direction)

    def set_speed(self, speed):
        self.speed.duty_u16(speed)


class Trainset:
    def __init__(self):
        self.sensors = {}
        for s in Layout.sensors:
            self.sensors[s] = Sensor(Layout.sensors[s], s)
        self.points = {}
        for r in Layout.relays:
            #Initiate self.relays with all relays to up
            self.points[r] = Point(Layout.relays[r])
        self.tracks = {}
        for t in Layout.tracks:
            self.tracks[t] = Track(Layout.tracks[t])

    def run_train(self):
        self.tracks["A"].set_direction(True)
        self.tracks["A"].set_speed(30000)
        sleep(20)
        self.tracks["A"].set_speed(0)


t = Trainset()
t.run_train()



