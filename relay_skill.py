#!/usr/bin/env python3
from flask import Flask
from flask_ask import Ask, statement, question, session
from datetime import datetime, time, date, timedelta
import threading
import time

import RPi.GPIO as GPIO
import logging
from logging.handlers import RotatingFileHandler

pins = [10, 23, 25, 27, 8, 18, 7, 19, 24, 26, 5, 16, 12, 21, 13, 20]
devices = {
        "AC":16,
        "air conditioner":16
        }

app = Flask(__name__)
relay = Ask(app, "/relay")

#@app.route('/')
#def homepage():
#    return "Hello world"

convert_map = {
        'relay_number': int,
        'time': 'time',
        'duration': 'timedelta'
        }

@relay.launch
def start_relay():
    return question("which device?")

@relay.intent("AllOn")
def relay_allon():
    app.logger.info('Turning on ALL the relays')
    for p in pins:
        GPIO.output(p, GPIO.HIGH)
    return statement("okay")

@relay.intent("AllOff")
def relay_alloff():
    app.logger.info('Turning on ALL the relays')
    for p in pins:
        GPIO.output(p, GPIO.LOW)
    return statement("okay")

@relay.intent("On", convert=convert_map)
def relay_on(device, relay_number, time, duration):

    if device:
        relay_number = devices[device]

    if not duration == None:
        gpio_on_duration(relay_number, duration.seconds)
    elif not time == None:
        now = datetime.now() - timedelta(minutes=300)
        target = datetime.combine(now, time)
        if now.time() > time:
            target = target + timedelta(1, 0)
        gpio_on_delay(relay_number, (target-now).seconds)
    else:
        gpio_on(relay_number)

    return statement("okay")

@relay.intent("Off", convert=convert_map)
def relay_off(device, relay_number, time, duration):

    if device:
        relay_number = devices[device]

    if not duration == None:
        gpio_off_duration(relay_number, duration.seconds)
    elif not time == None:
        now = datetime.now() - timedelta(minutes=300)
        target = datetime.combine(now, time)
        if now.time() > time:
            target = target + timedelta(1, 0)
        gpio_off_delay(relay_number, (target-now).seconds)
    else:
        gpio_off(relay_number)

    return statement("okay")

@relay.intent("Toggle", convert=convert_map)
def relay_toggle(device, relay_number):

    if device:
        relay_number = devices[device]

    if GPIO.input(pins[relay_number-1]) == 1:
        gpio_off(relay_number)
    else:
        gpio_on(relay_number)

    return statement("okay")

@relay.intent("AMAZON.FallbackIntent")
def fallback():
    return question("Sorry, I didn't understand that. Which?")

@relay.intent("AMAZON.StopIntent")
def stop():
    return statement("ok")

@relay.intent("AMAZON.CancelIntent")
def cancel():
    return statement("ok")

@relay.intent("AMAZON.HelpIntent")
def help():
    return statement("feature not implemented yet. go yell at brian")

def gpio_on_delay(relay_num, sec):
    app.logger.info("Turning on relay #{} after {} seconds".format(relay_num, sec))
    threading.Timer(sec, gpio_on, [relay_num]).start()

def gpio_off_delay(relay_num, sec):
    app.logger.info("Turning off relay #{} after {} seconds".format(relay_num, sec))
    threading.Timer(sec, gpio_off, [relay_num]).start()

def gpio_on_duration(relay_num, sec):
    app.logger.info("Turning on relay #{} for {} seconds".format(relay_num, sec))
    GPIO.output(pins[relay_num-1], GPIO.HIGH)
    threading.Timer(sec, gpio_off, [relay_num]).start()

def gpio_off_duration(relay_num, sec):
    app.logger.info("Turning off relay #{} for {} seconds".format(relay_num, sec))
    GPIO.output(pins[relay_num-1], GPIO.LOW)
    threading.Timer(sec, gpio_on, [relay_num]).start()

def gpio_on(relay_num):
    app.logger.info('Turning on relay #{}'.format(relay_num))
    GPIO.output(pins[relay_num-1], GPIO.HIGH)

def gpio_off(relay_num):
    app.logger.info('Turning off relay #{}'.format(relay_num))
    GPIO.output(pins[relay_num-1], GPIO.LOW)

def main():
    GPIO.setmode(GPIO.BCM)
    for p in pins:
        GPIO.setup(p, GPIO.OUT, initial=0)

    #logging.basicConfig(filename="relay.log", level=logging.DEBUG)

    try:
        handler = RotatingFileHandler('relay.log', maxBytes=10240)
        handler.setLevel(logging.DEBUG)
        app.logger.addHandler(handler)
        app.run(debug=True, use_reloader=False, host='0.0.0.0')
    finally:
        app.logger.info("Cleaning up")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
