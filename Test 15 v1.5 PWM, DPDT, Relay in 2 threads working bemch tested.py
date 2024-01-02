# Pronduction program running in threads 0 and 1 for Passing Loop
# GPIO pins used:
# P1  GPIO  0
# P2  GPIO  1
# P3  ++++ GROUND
# P4  GPIO  2
# P5  GPIO  3
# P6  GPIO  4
# P7  GPIO  5
# P8  ++++ GROUND
# P9  GPIO  6 
# P10 GPIO  7
# P11 GPIO  8 sensorS1
# P12 GPIO  9 sensorS2
# P13 ++++ GROUND
# P14 GPIO 10 sensorS3
# P15 GPIO 11 sensorS4
# P16 GPIO 12 sensorS5
# P17 GPIO 13 sensorS6
# P18 ++++ GROUND
# P19 GPIO 14 sensorS7
# P20 GPIO 15 sensorS8

# P21 GPIO 16 PWM_Track_2	
# P22 GPIO 17 Track_2B
# P23 ++++ GROUND
# P24 GPIO 18 Track_2A
# P25 GPIO 19 Track_1B
# P26 GPIO 20 Track_1A
# P27 GPIO 21 PWM_Track_1
# P28 ++++ GROUND
# P29 GPIO 22 Polarity_Trigger1
# P30 ++++ RUN
# P31 GPIO 26 Polarity_Trigger2
# P32 GPIO 27 Relay_P1_DOWN
# P33 ++++ GROUND
# P34 GPIO 28 Relay_P1_UP
# P35 ++++ ADC VREF
# P36 ++++ 3.3V OUT
# P37 ++++ 3.3V EN
# P38 ++++ GROUND
# P39 ++++ VSYS
# P40 ++++ VBUS

from machine import Pin, PWM
from time import sleep
import _thread
import gc        #garbage collection to stop freezing
import random

####   set global variables
global Delay_Time_0
global Delay_Time_1
global Down_Train_in_Loop
global Down_Loop_Clear_Ahead
global Half_Cycle_Complete
global Cycle_Complete
global Down_Train_Arrived

#   Set track PWM pins and initial values
Track1_Speed = PWM(Pin(16))
Track1_Speed.freq(1000)
Track1_Speed.duty_u16(0)

Track2_Speed = PWM(Pin(21))
Track2_Speed.freq(1000)
Track2_Speed.duty_u16(0)


Track1a = Pin(17, Pin.OUT)
Track1a.low()
Track1b = Pin(18, Pin.OUT)
Track1b.low()

Track2a = Pin(19, Pin.OUT)
Track2a.low()
Track2b = Pin(20, Pin.OUT)
Track2b.low()

#   Set sensor pins
sensorS1 = Pin(8, Pin.IN, Pin.PULL_UP)
sensorS4 = Pin(11, Pin.IN, Pin.PULL_UP)
sensorS5 = Pin(12, Pin.IN, Pin.PULL_UP)
sensorS8 = Pin(15, Pin.IN, Pin.PULL_UP)

#   Set point and loop polarity pins and initialise
Relay_P1_UP = Pin(28,Pin.OUT)
Relay_P1_UP.value(1)
Relay_P1_DOWN = Pin(27,Pin.OUT)
Relay_P1_DOWN.value(1)

Loop_Polarity_Trigger1 = Pin(26,Pin.OUT)
Loop_Polarity_Trigger1.value(1)
Loop_Polarity_Trigger2 = Pin(22,Pin.OUT)
Loop_Polarity_Trigger2.value(1)

####   set initial variable values
MinSpeed = 8400
MaxSpeed = 8401
SpeedStep = 700
SpeedStep2 = -1000
CurrentSpeed = 0

Delay_Time_0 = 0
Delay_Time_1 = 0
Down_Train_in_Loop = False
Down_Loop_Clear_Ahead = False
Half_Cycle_Complete = False
Cycle_Complete = False
Down_Train_Arrived = False

####   define sub routines
def Track_Direction_UP_DOWN(Track, UpDown):
    if Track == 1:
        if UpDown == "UP":
            Track1a.high()
            Track1b.low()
        else:
            Track1a.low()
            Track1b.high()
    else:
        if UpDown == "UP":
            Track2a.high()
            Track2b.low()
        else:
            Track2a.low()
            Track2b.high() 

def Track_START(Track):
    if Track == 1:
        Track1_Speed.duty_u16(31000)
    else:
        Track2_Speed.duty_u16(32000)

def Track_STOP(Track):
    if Track == 1:
        Track1_Speed.duty_u16(0)
        Track1a.low()
        Track1b.low()
    else:
        Track2_Speed.duty_u16(0)
        Track2a.low()
        Track2b.low()
        
def Wait_For_Down_Loop():
    global Down_Train_in_Loop
    while Down_Train_in_Loop == False:
        sleep(0.2)
    print("Both trains arrived")

    Half_Cycle_Complete = True

def Switch_Points(Up_Down):
    print("up-down", Up_Down)
    sleep(1)
    print
    if Up_Down == 1:
        Relay_P1_DOWN.value(1)
        sleep(0.2)
        Relay_P1_UP.value(0)
    else:
        Relay_P1_UP.value(1)
        sleep(0.2)
        Relay_P1_DOWN.value(0)
    pass

def Toggle_Loop_Polarity(Direction):
    Track1a.low()
    Track1b.low()
    Track1_Speed.duty_u16(0)
    Track2a.low()
    Track2b.low()
    Track2_Speed.duty_u16(0)
    if Direction == 1:
        Loop_Polarity_Trigger2.value(0)
        Loop_Polarity_Trigger1.value(0)
    else:
        Loop_Polarity_Trigger1.value(1)
        Loop_Polarity_Trigger2.value(1)

def Run_Garbage_Collection():
    gc.collect()

####   Define thread operation ZERO
#############################################################################################
def core0_thread_up():
####   set global variables
    global Delay_Time_0
    global Down_Train_in_Loop
    global Down_Loop_Clear_Ahead
    global Half_Cycle_Complete
    global Cycle_Complete

#### wait random time before starting
    Delay_Time_0 = random.uniform(1, 10)
    sleep(Delay_Time_0)
    print(Delay_Time_0)
    
#### start up train
    Track_Direction_UP_DOWN(1, "UP")
    Track_START(1)
    print("Up train starting")
    
#### wait for sensor4 - up train arriving in loop
    while sensorS4.value():
        sleep(0.2)
    Track_STOP(1)
    print("Up train waiting in loop")
    
#### wait for core 1 to finish - down train arriving in loop
    while Down_Train_in_Loop == False:
        sleep(0.2)

#####   set up for completing cycle
    Half_Cycle_Complete = True
    Switch_Points(2)
    Toggle_Loop_Polarity(2)   ## sets current to tracks at zero whie polarity switching takes place
    Track_Direction_UP_DOWN(2, "UP")
    Track_Direction_UP_DOWN(1, "DOWN")
    Down_Loop_Clear_Ahead = True
    
    print("Both trains arrived, all set for departure from loop")

#### set random delay before Up train departs loop - minimum 2 secs
    Delay_Time_0 = 2 + random.uniform(1, 10)
    sleep(Delay_Time_0)
    
    print("Up train leaving loop")
    Track_START(2)
    
    print("sensorS8 ! ", sensorS8.value())
    while sensorS8.value() == 1:
        print("sensorS8 ! ", sensorS8.value())
        sleep(0.2)
    print("sensorS8 ! ", sensorS8.value())
    Track_STOP(2)
    
    print("Up train has reached destination")
    
#### wait for down train to arrive then house keep ready for next cycle
    while Down_Train_Arrived == False:
        pass
    print("Both trains reached destination - housekeeping for next cycle")
    
#### Housekeeping
    Switch_Points(1)
    Toggle_Loop_Polarity(1)
    Cycle_Complete = True
    Run_Garbage_Collection()
    Track_Direction_UP_DOWN(1, "UP")
    Track_Direction_UP_DOWN(2, "DOWN")

#
#CORE 1
#######################################################################################################
def core1_thread_down():
    global Delay_Time_1
    global Down_Train_in_Loop
    global Down_Loop_Clear_Ahead
    global Half_Cycle_Complete
    global Cycle_Complete
    global Down_Train_Arrived

#### wait random time before starting - minimum 1 sec
    Delay_Time_1 = 1 + random.uniform(1, 10)  
    sleep(Delay_Time_1)

#### start up train    
    Track_Direction_UP_DOWN(2, "DOWN")
    Track_START(2)
    print("Down train starting")
    
#### wait for sensor5 - down train arriving in loop, stop train and notify arrived
    while sensorS5.value():
        sleep(0.2)
    Track_STOP(2)
    Down_Train_in_Loop = True
    print("Down loco waiting in loop")

#### wait for clearance to proceed
    while Down_Loop_Clear_Ahead == False:
        pass
        
#### Ok to depart, wait random time before starting - minimum 2 sec
    Delay_Time_1 = 2 + random.uniform(1, 10)  
    sleep(Delay_Time_1)

#### Down train departing
#    Track_Direction_UP_DOWN(1, "DOWN")
    Track_START(1)
    print("Down train leaving loop")
    sleep(4
          
          
          
          )
    while not sensorS1.value():
        sleep(0.2)
        
    Track_STOP(1)
    
    print("Down train has reached destination")
    Down_Train_Arrived = True
    Run_Garbage_Collection()
    
#############################################################################################################
#Set system for start. Engines must be at the ends of the track start core 0
############################################################################################## Initial Housekeeping
Switch_Points(1)
Toggle_Loop_Polarity(1)
Run_Garbage_Collection()


while True:
    print("Starting new cycle ...")
    Cycle_Complete = False
    Half_Cycle_Complete = False
    second_thread = _thread.start_new_thread(core1_thread_down,())
    core0_thread_up()
