# Amazon Alexa Relay Control Skill

An Alexa skill to control a bunch of relays hooked up to a Raspberry Pi

The 'pins' list maps the relay to the GPIO pins on the Raspberry Pi.
The relay module used was those 16-channel 12V relay module interface board.
A custom bridge was built to connect the relay board to the RPi since the RPi output 3.3v logic levels and the relay board expects 5v logic level.
A one-way logic shifter was built using a single BS170 N-channel MOSFET for each channel.

The 'devices' list maps custom devices to a relay number.
This projects was meant to control a power strip.

The 'time_offset' variable is for my timezone (EST), which is 5 hours behind UTC.

The Alexa part uses the [Flask-ASK](https://github.com/johnwheeler/flask-ask) (Alexa Skills Kit) extension of the [Flask](http://flask.pocoo.org) framework.
So that probably has to be install.

To run:
```
./relay_skill.py
```

It will bind to port 5000.
For development and local uses, I have [ngrok](https://ngrok.com) set up and have the endpoint pointed to that.
All this is running on a tmux session on a Raspberry Pi.
