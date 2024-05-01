# [UV-Environment-Tracker]

This project is an implementation of an IoT UV sensor using an Mbed and Raspberry Pi 4. The Mbed uses a combination of motor control outputs and I2C communication to collect data and transmit the data via UART to a Raspberry Pi. The Pi then accumulates the data while simultaneously running a Flask server that allows the user to see how UV light levels change over time, minute by minute, and how each wavelength of UV light changes independently.

### Team Members:
- Rithvi Ravichandran
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

The Mbed in this project was chosen to simplify the I2C communication with the AS7331. Additionally, it was able to control the motor using 4 digital outputs through the ULN2003 Stepper Motor Driver

<img src="https://github.com/hchoi391/UV-Environment-Tracker/assets/90736210/f7174bef-985c-47cf-8dfe-8bd23ec35172" width="400" height="300">

[Link to mbed LPC1768](https://os.mbed.com/platforms/mbed-LPC1768/).

### 3. Raspberry Pi 4

The Raspberry Pi 4 is a great single-board computer that can be used to easily connect to a network and host a web server. We use it here to host a website using Flask, HTML, CSS, and Javascript. Additionally, it is able to take in
UART data from the Mbed and store it in JSON format for easy use on the webpage.

<img src="https://github.com/hchoi391/UV-Environment-Tracker/assets/90736210/69a8b329-fd78-4333-a6cc-4aefb896c143" width="500" height="300">

[Link to Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/).

### 4. 28BYJ-48 4-Phase Stepper Motor

The 4-phase stepper motor provides high accuracy and precision for rotation angles and provides the ability to rotate continuously, bi-directionally. It is used, in addition to a motor shaft coupler, to angle the UV sensor 45-degrees upwards and rotate it
360 degrees to get a line of sight to the whole room from where the device was placed. 

<img src="https://github.com/hchoi391/UV-Environment-Tracker/assets/29440172/152001e7-de64-456c-96e9-6dbd32be9669" width="300" height="300">

<img src="https://github.com/hchoi391/UV-Environment-Tracker/assets/90736210/5801859e-c4f4-436c-bdad-547ed5fab607" width="300" height="300">

[Link to 28BYJ-48 - 5V Stepper Motor](https://components101.com/motors/28byj-48-stepper-motor).

### 5. ULN2003 Stepper Motor Driver

By using 4 digital ouputs from the Mbed, we can control the stepper motor speed, direction, and amount of steps. 

<img src="https://github.com/hchoi391/UV-Environment-Tracker/assets/29440172/152001e7-de64-456c-96e9-6dbd32be9669" width="250" height="220">


[Link to ULN2003 Stepper Motor Driver](https://lastminuteengineers.com/28byj48-stepper-motor-arduino-tutorial/).

# ----- Setup Intruction -----
## Wiring

- ### Mbed

|   Mbed   | AS7331 Breakout |
| -------- | ------- |
| p9  | SDA    |
| p10 | SCL     |
| VOUT    | 3.3V    |
| GND     | GND |
| p21    | INT |

| Mbed | ULN2003 Breakout |
| -------| -------- |
| p14 | IN1 |
| p15 | IN2 |
| p16 | IN3 |
| p17 | IN4 |

| Other | Device | Pin | Notes |
| --- | --- | --- | --- |
| Mbed| Pushbutton | p20 | Connect button to ground |
| External +5V | Stepper Driver Board | (+) Input | Connect adjacent pin to ground |

- ### Raspberry Pi

| Raspberry Pi | Mbed |
| --- | --- |
| USB-A Port | USB Mini-B Port |

## Library Download

- ### Flask
- ### SocketIO


# ----- How to Run -----

### 1. Mbed Setup

Create a new Mbed project in Keil Studio. Copy and paste the [main.cpp](https://github.com/hchoi391/UV-Environment-Tracker/blob/aa5a50ba430a5613edb88fa920b52be83db5d55a/mbed_firmware/main.cpp) file in mbed_firmware into the main.cpp file created by Keil.

The following libraries are required and can be added through Keil through the Mbed libraries tab.

| Name | Link |
| --- | --- |
| PinDetect | [Link](http://os.mbed.com/users/AjK/code/PinDetect/) |
| sMotor | [Link](http://os.mbed.com/users/XtaticO/code/sMotor/) |

Select your device and build target on the left side, build the project, and transfer the file to the connected Mbed. 

<img src="https://github.com/hchoi391/UV-Environment-Tracker/assets/29440172/071c7c9f-b805-4e94-8c0b-095f76ec04bf" width="250" height="220">

Reset the Mbed and plug it into the Raspberry Pi's USB-A port.

### 2. Raspberry Pi Setup

Copy the [pi_server](https://github.com/hchoi391/UV-Environment-Tracker/tree/c7013147d60fc9a96ca2154a3c8f3967193979f1/pi_server) folder onto your Pi. 

Connect your Pi to the local WiFi network. Whichever computer that is being used to connect to the Pi's webpage should be connected to the same network.

### 3. Collecting data

To collect UV data, make sure the Mbed and all the components are wired correctly and the Mbed is plugged into the Pi.

On the Pi, navigate to the pi_server directory. Run monitor_serial.py using ```python monitor_serial.py```

Press the pushbutton to start the data collection. You should see output in the terminal as the Mbed is sending data over the COM port. Press the pushbutton at any time again to stop data collection and save the data.

### 4. Running the Web Server and connecting

Now that there is data available, run the web server by navigating to the pi_server directory. Run ```python app.py``` to run the server. Take note of the IP address that is displayed and port and type that into a browser.

<img src="https://github.com/hchoi391/UV-Environment-Tracker/assets/29440172/56d591da-5999-4b1e-8115-d7bc37180ea4" width="800" height="250">

Use the IP address that is not ```127.0.0.1``` to connect to the webpage from a different computer.

Now you should be able to visualize your data over time.


# ----- Demo Video -----

[Link to Youtube Video](https://youtu.be/naTzLh4TvLk)

# ----- Pictures of Example UV map -----

![image](https://github.com/hchoi391/UV-Environment-Tracker/assets/90736210/e69ac7c0-04c8-4dbd-b23c-fb167be8be89)
