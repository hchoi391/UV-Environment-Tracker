# [UV-Environment-Tracker]

This project is an implementation of an IoT UV sensor using an Mbed and Raspberry Pi 4. The Mbed uses a combination of motor control outputs and I2C communication to collect data and transmit the data via UART to a Raspberry Pi. The Pi then accumulates the data while simultaneously running a Flask server that allows the user to see how UV light levels change over time, minute by minute, and how each wavelength of UV light changes independently.

### Team Members:
- Rithvi Raj Ravichandran
- Huijun Choi

# ----- Outline -----
- List of Components
  - Sparkfun AS7331 UV Sensor Breakout Board
  - Mbed LPC1768
  - Raspberry Pi 4
  - 28BYJ-48 4-Phase Stepper Motor
  - ULN2003 Stepper Motor Driver
- Setup Instruction
  - Wiring
  - Library Download
- How to Run
- Demo Video
- Pictures of Example UV map

# ----- List of Components -----

### 1. Sparkfun AS7331 UV Sensor Breakout Board

The UV sensor is a 3-channel AS7331 by ams-OSRAM. It is a low-power, low-noise UV sensor capable of reading UVA, UVB, and UVC channels and converting those radiation levels to a digital result. The chip has adjustable gain, conversion time, and different measurement modes. The chip communicates via I2C and stores a 16-bit integer as the measured value for each respective channel.

<img src="https://github.com/hchoi391/UV-Environment-Tracker/assets/90736210/95c0a19f-0442-4861-87e1-ae759edc6a24" width="200" height="150">

[Link to SparkFun Mini Spectral UV Sensor - AS7331 (Qwiic)](https://www.sparkfun.com/products/23518).

### 2. Mbed LPC1768

The Mbed in this project was chosen to simplify the I2C communication with the AS7331. Additionally, it was able to control the motor using 4 digital inputs through the ULN2003 Stepper Motor Driver

<img src="https://github.com/hchoi391/UV-Environment-Tracker/assets/90736210/f7174bef-985c-47cf-8dfe-8bd23ec35172" width="400" height="300">

[Link to mbed LPC1768](https://os.mbed.com/platforms/mbed-LPC1768/).

### 3. Raspberry Pi 4

temp

<img src="https://github.com/hchoi391/UV-Environment-Tracker/assets/90736210/69a8b329-fd78-4333-a6cc-4aefb896c143" width="500" height="300">

[Link to Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/).

### 4. 28BYJ-48 4-Phase Stepper Motor

temp 

<img src="https://github.com/hchoi391/UV-Environment-Tracker/assets/90736210/38e06aeb-5d86-482d-807f-7bc6ac47f22b" width="300" height="300">

<img src="https://github.com/hchoi391/UV-Environment-Tracker/assets/90736210/5801859e-c4f4-436c-bdad-547ed5fab607" width="300" height="300">

[Link to 28BYJ-48 - 5V Stepper Motor](https://components101.com/motors/28byj-48-stepper-motor).

### 5. ULN2003 Stepper Motor Driver

temp 

<img src="https://github.com/hchoi391/UV-Environment-Tracker/assets/90736210/1fef3114-ceaf-4bed-8baa-a8c64e0c2d4b" width="250" height="220">


[Link to ULN2003 Stepper Motor Driver](https://lastminuteengineers.com/28byj48-stepper-motor-arduino-tutorial/).

# ----- Setup Intruction -----
## Wiring

- ### Mbed
- ### Raspberry Pi

## Library Download

- ### Flask
- ### SocketIO


# ----- How to Run -----

### 1.
### 2.
### 3.
### 4.

# ----- Demo Video -----


# ----- Pictures of Example UV map -----
