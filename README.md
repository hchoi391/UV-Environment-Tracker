# UV-Environment-Tracker

This project is an implementation of an IoT UV sensor using an Mbed and Raspberry Pi 4. The Mbed uses a combination of motor control outputs and I2C communication to collect data and transmit the data via UART to a Raspberry Pi. The Pi then accumulates the data while simultaneously running a Flask server that allows the user to see how UV light levels change over time, minute by minute, and how each wavelength of UV light changes independently.

## Team Members:
Rithvi Raj Ravichandran
Huijun Choi


## Components:
1. Sparkfun AS7331 UV Sensor Breakout Board

The UV sensor is a 3-channel AS7331 by ams-OSRAM. It is a low-power, low-noise UV sensor capable of reading UVA, UVB, and UVC channels and converting those radiation levels to a digital result. The chip has adjustable gain, conversion time, and different measurement modes. The chip communicates via I2C and stores a 16-bit integer as the measured value for each respective channel.

2. Mbed LPC1768

The Mbed in this project was chosen to simplify the I2C communication with the AS7331. Additionally, it was able to control the motor using 4 digital inputs through the ULN2003 Stepper Motor Driver

3. Raspberry Pi 4

temp

4. 28BYJ-48 4-Phase Stepper Motor

temp 

5. ULN2003 Stepper Motor Driver

temp 

# Setup
## Wiring


