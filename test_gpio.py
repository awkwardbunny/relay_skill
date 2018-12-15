#!/usr/bin/env python3
import RPi.GPIO as GPIO
from time import sleep
import signal,sys,socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5250
BUF_SIZE = 512

pins = [10, 23, 25, 27, 8, 18, 7, 19, 24, 26, 5, 16, 12, 21, 13, 20]
states = [0] * len(pins)

def handler(signum, frame):
        print('Signal received:',signum)
        print('Shutting down...')
        for p in pins:
            GPIO.output(p, GPIO.LOW)
        GPIO.cleanup()
        sys.exit(0)

def main():
    signal.signal(signal.SIGINT, handler)

    GPIO.setmode(GPIO.BCM)
    for p in pins:
        GPIO.setup(p, GPIO.OUT)
    
    while True:
        for i in range(len(pins)):
            if states[i] == 0:
    	        GPIO.output(pins[i], GPIO.LOW)
            else:
    	        GPIO.output(pins[i], GPIO.HIGH)
    
    GPIO.cleanup()

if __name__ == "__main__":
    main()

