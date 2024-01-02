# Production program running in threads 0 and 1 for Passing Loop
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
# P29 GPIO 22  Relay_P1_UP
# P30 ++++ RUN
# P31 GPIO 26  Relay_P1_DOWN
# P32 GPIO 27 Polarity_Trigger1
# P33 ++++ GROUND
# P34 GPIO 28 Polarity_Trigger2
# P35 ++++ ADC VREF
# P36 ++++ 3.3V OUT
# P37 ++++ 3.3V EN
# P38 ++++ GROUND
# P39 ++++ VSYS
# P40 ++++ VBUS

tracks = {'A':{'Speed':16, 'Signal_a':17, 'Signal_b':18}, 
               'B':{'Speed':21, 'Signal_a':19, 'Signal_b':20}}
sensors = {'S1':8, 'S4':11, 'S5':12, 'S8':15}
relays = {'P1':{'UP':22, 'DOWN':26}}

for t in tracks:
    print(f'Track {t} has Speed on pin {track[t]["Speed"]}, signal_a on pin {track[t]["Signal_a"]} and signal_b on pin {track[t]["Signal_b"]}')

for s in sensors:
    print(f'Sensor {s} is on pin {sensors[s]}')

for r in relays:
    print(f'Relay {r} is up on {relays[r]["UP"]} and down on pin {relays[r]["DOWN"]}')