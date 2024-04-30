#include "mbed.h"
#include "Stepper.h"
#include "PinDetect.h"
#include "sMotor.h"
 
Serial pc(USBTX, USBRX);
I2C i2c(p9, p10);

Stepper stepper (p14, p15, p16, p17);   
sMotor motor(p14, p15, p16, p17); 

int step_speed = 1200 ; // set default motor speed
int num_steps = 8; //1/64th of the total rotation

volatile int state = 0;
PinDetect pb(p20, PullUp);
float angle = 0.0;

int last_pb_state = 0;

Ticker motorTicker;
volatile int attached = 0;

uint16_t A =0;
uint16_t B = 0;
uint16_t C = 0;

char measA[2];
char measB[2];
char measC[2];

char aAddr[1] = {0x02};
char bAddr[1] = {0x03};
char cAddr[1] = {0x04};

volatile float interval = 5.625;
volatile bool stepperDir = true;

DigitalIn ready(p21);

#define AS7331_ADDR 0xE8 // I2C slave address

void collectMeasurement(float currAngle){
    i2c.write(AS7331_ADDR, aAddr, 1, true);
    i2c.read(AS7331_ADDR, measA, 2);
    A = 0;
    A |= (uint16_t)measA[1] << 8;
    A |= (uint16_t)measA[0];

    i2c.write(AS7331_ADDR, bAddr, 1, true);
    i2c.read(AS7331_ADDR, measB, 2);
    B = 0;
    B |= (uint16_t)measB[1] << 8;
    B |= (uint16_t)measB[0];

    i2c.write(AS7331_ADDR, cAddr, 1, true);
    i2c.read(AS7331_ADDR, measC, 2);
    C = 0;
    C |= (uint16_t)measC[1] << 8;
    C |= (uint16_t)measC[0];

    pc.printf("angle,%.3f,A,%d,B,%d,C,%d\n",currAngle, A, B, C);
}

void restartMeasurement(){
    char config_data[2] = {
        0x00,
        0x80
    };
    i2c.write(AS7331_ADDR, config_data, 2);
}

void stopMeasurement() {
    char end_data[2];

    end_data[0] = 0x00;
    end_data[1] = 0x43;
    i2c.write(AS7331_ADDR, end_data, 2);
}

void moveMotor(){
    if (stepperDir && angle == 360.0) {
        stepperDir = !stepperDir;
        interval = interval*-1.0;
    } else if (!stepperDir && angle == 0.0) {
        stepperDir = !stepperDir;
        interval = interval*-1.0;
    }

    motor.step(num_steps, stepperDir, step_speed);
    angle += interval;

    // printf("angle: %f\n", angle);
}

void keyReleased(){
    state = !state;
    if (state){
        pc.printf("Start\n");
    } else {
        pc.printf("End\n");
    }
}

void setup() {
    i2c.frequency(400000); // Set I2C frequency to 400kHz
    pb.mode(PullUp);
    wait(0.001);
    pb.attach_deasserted( &keyReleased );
    pb.setSampleFrequency();

    //Software Reset
    char init_data[2];

    init_data[0] = 0x00;
    init_data[1] = 0x0a;
    i2c.write(AS7331_ADDR, init_data, 2);

    // Set Gain and Conversion Time (512ms)
    init_data[0] = 0x06;
    init_data[1] = 0x58;
    i2c.write(AS7331_ADDR, init_data, 2);
}
 
int main()
{   
    setup();
    while(1){
        if (state == 0) {
            motorTicker.detach();
            stopMeasurement();
        } else if (state == 1) {
            char start_data[2];

            start_data[0] = 0x00;
            start_data[1] = 0x83;
            i2c.write(AS7331_ADDR, start_data, 2);

            motorTicker.attach(&moveMotor, 0.75);

            int temp = 0;
            while(state == 1){
                temp = ready.read();
                if (temp == 1){
                    collectMeasurement(angle);
                    restartMeasurement();
                }
            }
        }
    }
}