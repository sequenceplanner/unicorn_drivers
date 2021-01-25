#include "TrashActuator.h"
#include "Arduino.h"

TrashActuator::TrashActuator(uint8_t IN1, uint8_t IN2, unsigned long actuationTime) {
    this->IN1 = IN1;
    this->IN2 = IN2;
    this->actuationTime = actuationTime;

    //set up pin outputs
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);

    //set up initial command and output to COAST
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);

    currentCommand = ACTUATOR_CMD_COAST;

    //initial position when starting is unknown
    actuatorState = ACTUATOR_UNKOWN;

}

void TrashActuator::setActuatorCommand(uint8_t command, unsigned long currentTime) {
    //Serial.println(F("Setting command"));
    if(command == currentCommand) {
        return; //ignore repeated same command
    }
    else {
        currentCommand = command;
    }

    switch (command)
    {
    case ACTUATOR_CMD_UP:
        prevTime = currentTime; //sets timer
        actuatorState = ACTUATOR_UNKOWN;
        //set motor outputs:
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        break;

    case ACTUATOR_CMD_DOWN:
        //Serial.println(F("CMD: DOWM"));
        prevTime = currentTime; //sets timer
        actuatorState = ACTUATOR_UNKOWN;
        //set motor outputs:
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        break;

    case ACTUATOR_CMD_COAST:
        actuatorState = ACTUATOR_UNKOWN;
        //set motor outputs:
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        break;

    default:
        //invalid command
        Serial.println(F("ERROR: INVALID COMMAND"));
        break;
    }
}

uint8_t TrashActuator::getActuatorState(unsigned long currentTime) {
    //check if time delta is longer than actuationTime
    if (currentTime - prevTime > actuationTime) {
        switch (currentCommand)
        {
        case ACTUATOR_CMD_DOWN:
            actuatorState = ACTUATOR_DOWN;
            currentCommand = ACTUATOR_CMD_COAST;
            //set motor outputs:
            digitalWrite(IN1, LOW);
            digitalWrite(IN2, LOW);
            break;
        case ACTUATOR_CMD_UP:
            actuatorState = ACTUATOR_UP;
            currentCommand = ACTUATOR_CMD_COAST;
            //set motor outputs:
            digitalWrite(IN1, LOW);
            digitalWrite(IN2, LOW);
            break;
        default:
            break;
        }
    }

    return actuatorState;
}