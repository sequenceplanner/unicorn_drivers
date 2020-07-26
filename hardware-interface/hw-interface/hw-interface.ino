#include "src/Adafruit-VL530X/Adafruit_VL53L0X.h"
#include "TrashActuator.h"

//defenition of serial commands:
#define CMD_UP 'U'
#define CMD_DOWN 'D'
#define CMD_COAST 'C'
#define GET_STATE 'S'

// address we will assign if dual sensor is present
#define LOXR_ADDRESS 0x30
#define LOXF_ADDRESS 0x31
// last one will be left with default adress 0x29

// set the pins to shutdown
#define SHT_LOXR A3 //right 
#define SHT_LOXF 3 //front (diode connected)
#define SHT_LOXL 2 //left  (diode connected)

//define sensor states
#define LOX_OUT_OF_RANGE 4

// objects for the vl53l0x
Adafruit_VL53L0X loxRight = Adafruit_VL53L0X();
Adafruit_VL53L0X loxFront = Adafruit_VL53L0X();
Adafruit_VL53L0X loxLeft = Adafruit_VL53L0X();

// set the pins for motor control
#define IN1 6
#define IN2 5

// sets actuation time in ms
#define ACTUATION_TIME 4000

// object for trash tipper
TrashActuator actuator = TrashActuator(IN1, IN2, ACTUATION_TIME);

//function prototypes:
void setID();
int readRange(Adafruit_VL53L0X *sensor);
//void initActuator();
//void setActuator(uint8_t mode);

void setup() {
  Serial.begin(115200);
  // wait until serial port opens for native USB devices:
  while (! Serial) { delay(1); }

  //configure adress for all 3 sensors:
  setID();

  //set actuator to down position
  actuator.setActuatorCommand(ACTUATOR_CMD_DOWN, millis());
  delay(ACTUATION_TIME);
}

void loop() {

  //set up local variables;
  static int rightRange, leftRange, frontRange;
  static unsigned long timeInterval;
  char cmd;

  cmd = Serial.read();

  switch (cmd)
  {
  case -1:
    break; //corresponds to no command
  case '\n':
    break; //ignore end of string
  case CMD_COAST:
    actuator.setActuatorCommand(ACTUATOR_CMD_COAST, millis());
    break;
  case CMD_UP:
    actuator.setActuatorCommand(ACTUATOR_CMD_UP, millis());
    break;
  case CMD_DOWN:
    actuator.setActuatorCommand(ACTUATOR_CMD_DOWN, millis());
    break;
  case GET_STATE:
    Serial.println(actuator.getActuatorState(millis()));
    break;
  default:
    Serial.println(F("INVALID CMD"));
    break;
  }

  /*
  //read distances:
  timeInterval = millis();
  rightRange = readRange(&loxRight);
  leftRange = readRange(&loxLeft);
  frontRange = readRange(&loxFront);
  timeInterval = millis() - timeInterval;
  Serial.println(timeInterval);

  //output range over serial:
  /*
  Serial.print(F("R: "));
  Serial.println(rightRange);
  Serial.print(F("L: "));
  Serial.println(leftRange);
  Serial.print(F("F: "));
  Serial.println(frontRange);
  /*
  Serial.print(F("Sensor right: "));
  Serial.println(readRange(&loxRight));
  Serial.print(F("Sensor front: "));
  Serial.println(readRange(&loxFront));
  Serial.print(F("Sensor left: "));
  Serial.println(readRange(&loxLeft));
  */  
}


void setID() {
  // shutdown all sensors:
  pinMode(SHT_LOXR, OUTPUT);
  pinMode(SHT_LOXF, OUTPUT);
  pinMode(SHT_LOXL, OUTPUT);

  digitalWrite(SHT_LOXR, LOW);
  digitalWrite(SHT_LOXF, LOW);
  digitalWrite(SHT_LOXL, LOW);

  delay(100);

  // enable right sensor:
  pinMode(SHT_LOXR, INPUT);
  delay(10);

  // initing right
  if(!loxRight.begin(LOXR_ADDRESS)) {
    Serial.println(F("Right failed"));
    while(1);
  }
  delay(10);

  //enable front sensor:
  pinMode(SHT_LOXF, INPUT);
  delay(10);

  //initing front
  if(!loxFront.begin(LOXF_ADDRESS)) {
    Serial.println(F("Front failed"));
    while(1);
  }
  delay(10);

  //enable left sensor
  pinMode(SHT_LOXL, INPUT);
  delay(10);
  
  //initing left (default adress)
  if(!loxLeft.begin()) {
    Serial.println(F("Left failed"));
    while(1);
  }
  delay(10);
}

int readRange(Adafruit_VL53L0X *sensor) {
  // returns -1 if sensor is out of range
  // returns range  in mm if sensor is in range
  // this holds the measurement (what is this struct -  how much memmory?)
  static VL53L0X_RangingMeasurementData_t measurement;
  // get measurement with debug disabled
  sensor->getSingleRangingMeasurement(&measurement, false);
  if(measurement.RangeStatus != LOX_OUT_OF_RANGE) {
    return measurement.RangeMilliMeter;
  }
  else {
    return -1;
  }
}
/*
void initActuator() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  setActuator(ACTUATOR_DOWN);
}

void setActuator(uint8_t mode) {
  switch (mode) {
  case ACTUATOR_COAST:
    Serial.println(F("COAST"));
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    break;
  case ACTUATOR_UP:
    Serial.println(F("UP"));
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    break;
  case ACTUATOR_DOWN:
    Serial.println(F("DOWN"));
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    break;
  default: //default to coast (ie do nothing)
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    break;
  }
}
*/