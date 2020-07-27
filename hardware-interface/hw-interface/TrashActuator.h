#ifndef _TRASH_ACTUATOR_H
#define _TRASH_ACTUATOR_H

#include <stdint.h>

// define actuator control commands (see table 1 DRV8871 datasheet)
#define ACTUATOR_CMD_COAST 0
#define ACTUATOR_CMD_UP 1
#define ACTUATOR_CMD_DOWN 2

// define actuator states
#define ACTUATOR_UNKOWN 0
#define ACTUATOR_UP 1
#define ACTUATOR_DOWN 2

class TrashActuator {
    public:
    //default constructor (takes connected pins as input):
    TrashActuator(uint8_t IN1, uint8_t IN2, unsigned long actuationTime);

    uint8_t getActuatorState(unsigned long currentTime); //call using millis()
    void setActuatorCommand(uint8_t command, unsigned long currentTime);

    private:
    uint8_t IN1, IN2;
    uint8_t actuatorState;
    uint8_t currentCommand;
    unsigned long prevTime;      //tracks timing of state transitions
    unsigned long actuationTime; //time to wait before state transition
};

#endif