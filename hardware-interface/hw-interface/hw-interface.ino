#include "src/Adafruit-VL530X/Adafruit_VL53L0X.h"
#include "TrashActuator.h"

//all serial commands are sent in a single byte where only the latest
//command is considered

#define NEWLINE "\n"

//defenition of serial commands:
#define ACTUATOR_MASK   0b00000011
#define ACTUATOR_SHIFT  0
#define COLOR_MASK      0b00011100
#define COLOR_SHIFT     2

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
#define LOX_ERROR -2

// objects for the vl53l0x
Adafruit_VL53L0X loxRight = Adafruit_VL53L0X();
Adafruit_VL53L0X loxFront = Adafruit_VL53L0X();
Adafruit_VL53L0X loxLeft = Adafruit_VL53L0X();

//define pins for indicator light
#define R_OUT (uint8_t)8
#define G_OUT (uint8_t)9
#define B_OUT (uint8_t)10

//define colors for indicator light
#define INDICATOR_OFF 0
#define INDICATOR_RED 1
#define INDICATOR_BLUE 2
#define INDICATOR_GREEN 3
#define INDICATOR_YELLOW 4
#define INDICATOR_WHITE 5

//global variable for current color
uint8_t currentColor;

//function prototypes for indicator light
void setColor(uint8_t color);
void initIndicator();

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

//pin defenitions for trash sensors
#define PROX_PIN1 11
#define PROX_PIN2 12

//trash status values
#define TRASH_FULL 1
#define TRASH_EMPTY 0
#define TRASH_FULL_PATTERN   0b00000011 //sets how many consequtive readings need to be the same for state switch
#define TRASH_EMPTY_PATTERN  0b00000000
#define TRASH_PATTERN_MASK   0b00000011 //sets how many consequtive readings need to be the same for state switch

void setup() {
  Serial.begin(115200);
  // wait until serial port opens for native USB devices:
  while (! Serial) { delay(1); }

  //configure adress for all 3 sensors:
  setID();

  //set actuator to down position
  actuator.setActuatorCommand(ACTUATOR_CMD_DOWN, millis());
  //delay(ACTUATION_TIME);

  //configure trash sensors pins as input:
  pinMode(PROX_PIN1, INPUT);
  pinMode(PROX_PIN2, INPUT);

  initIndicator();
  //testing colors:
  setColor(INDICATOR_RED);
  delay(100);
  setColor(INDICATOR_GREEN);
  delay(100);
  setColor(INDICATOR_BLUE);
  delay(100);
  setColor(INDICATOR_YELLOW);
  delay(100);
  setColor(INDICATOR_WHITE);
  delay(100);
  setColor(INDICATOR_GREEN);   //default standby color
}

void loop() {

  //set up static local variables;
  static int rightRange, leftRange, frontRange;
  static unsigned long timeInterval;
  static char tempCmd;
  static uint8_t cmd = 0;
  static uint8_t trashStatus;
  static uint8_t trashStatusDebounce = 0;
  static uint8_t cmdColor;
  static uint8_t cmdActuator;
  uint8_t prevCmd = cmd;

  // grab latest command (reads serial buffer until empty)
  while( (tempCmd = Serial.read()) != -1 ) {
    cmd = tempCmd;
  }

  //check if command has changed:
  if(cmd!=prevCmd) {
    // Serial.print(F("NEW CMD: "));
    // Serial.println(cmd, BIN);
    //parse commands:
    cmdActuator = (cmd & ACTUATOR_MASK) >> ACTUATOR_SHIFT;
    cmdColor = (cmd & COLOR_MASK) >> COLOR_SHIFT;
    // Serial.print(F("NEW CMD ACTUATOR: "));
    // Serial.println(cmdActuator, BIN);
    // Serial.print(F("NEW CMD COLOR: "));
    // Serial.println(cmdColor, BIN);

    //set commands:
    actuator.setActuatorCommand(cmdActuator, millis());
    setColor(cmdColor);
  }

  //read distances:
  rightRange = readRange(&loxRight);
  leftRange = readRange(&loxLeft);
  frontRange = readRange(&loxFront);

  //check sensor error status:
  while(rightRange == LOX_ERROR || leftRange == LOX_ERROR || frontRange == LOX_ERROR) {
    //reset sensors:
    setID();
    //read distances:
    rightRange = readRange(&loxRight);
    leftRange = readRange(&loxLeft);
    frontRange = readRange(&loxFront);
  }

  //read status of trash proximity sensors
  //if any of the sensor are active low then trash is considered detected

  if (!digitalRead(PROX_PIN1) || !digitalRead(PROX_PIN2)) {
    trashStatusDebounce = trashStatusDebounce << 1;
    trashStatusDebounce |= 1;
  }
  else {
    trashStatusDebounce = trashStatusDebounce << 1;
  }

  if ( (trashStatusDebounce & TRASH_PATTERN_MASK) == TRASH_FULL_PATTERN) {
    trashStatus = TRASH_FULL;
  }
  else if ( (trashStatusDebounce & TRASH_PATTERN_MASK) == TRASH_EMPTY_PATTERN) {
    trashStatus = TRASH_EMPTY;
  }

  //trash debounce debug:
/*   Serial.print("Trash Status: ");
  Serial.println(trashStatus);
  Serial.print("History: ");
  Serial.println(trashStatusDebounce, BIN); */
  
  //indicate start of packet
  Serial.print(F("PACKET:"));
  Serial.print(NEWLINE);
  //print range over serial:
  Serial.print(F("R: "));
  Serial.print(rightRange);
  Serial.print(NEWLINE);
  Serial.print(F("L: "));
  Serial.print(leftRange);
  Serial.print(NEWLINE);
  Serial.print(F("F: "));
  Serial.print(frontRange);
  Serial.print(NEWLINE);

  //print state of trash actuator
  Serial.print(F("A: "));
  Serial.print(actuator.getActuatorState(millis()));
  Serial.print(NEWLINE);

  //print state of trash carrying
  Serial.print(F("T: "));
  Serial.print(trashStatus);
  Serial.print(NEWLINE);

  //print state of ligt indicator
  Serial.print(F("I: "));
  Serial.print(currentColor);
  Serial.print(NEWLINE);
}


void setID() {
  Serial.println(F("Resetting sensors"));
  // shutdown all sensors:
  pinMode(SHT_LOXR, OUTPUT);
  pinMode(SHT_LOXF, OUTPUT);
  pinMode(SHT_LOXL, OUTPUT);

  digitalWrite(SHT_LOXR, LOW);
  digitalWrite(SHT_LOXF, LOW);
  digitalWrite(SHT_LOXL, LOW);

  delay(10);

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
  int status;
  // returns -1 if sensor is out of range
  // returns range  in mm if sensor is in range
  // this holds the measurement (what is this struct -  how much memmory?)
  static VL53L0X_RangingMeasurementData_t measurement;
  // get measurement with debug disabled
  status = sensor->getSingleRangingMeasurement(&measurement, false);
  //Serial.print(F("Status: "));
  //Serial.println(status);
  if(status == VL53L0X_ERROR_NONE) {
    if(measurement.RangeStatus != LOX_OUT_OF_RANGE) {
      return measurement.RangeMilliMeter;
    }
    else {
      return -1;
    }
  }
  else {
    //did not manage to read distance correctly
    return LOX_ERROR;
  }

}

void initIndicator() {
  pinMode(R_OUT, OUTPUT);
  pinMode(G_OUT, OUTPUT);
  pinMode(B_OUT, OUTPUT);

  digitalWrite(R_OUT, LOW);
  digitalWrite(G_OUT, LOW);
  digitalWrite(B_OUT, LOW);

  currentColor = INDICATOR_OFF;
}

void setColor(uint8_t color) {
    //Serial.println(F("Setting color"));
    currentColor = color;
    switch (color) {
    case INDICATOR_OFF:
      digitalWrite(R_OUT, LOW);
      digitalWrite(G_OUT, LOW);
      digitalWrite(B_OUT, LOW);
      break;

    case INDICATOR_RED:
      digitalWrite(R_OUT, HIGH);
      digitalWrite(G_OUT, LOW);
      digitalWrite(B_OUT, LOW);
      break;

    case INDICATOR_BLUE:
      digitalWrite(R_OUT, LOW);
      digitalWrite(G_OUT, LOW);
      digitalWrite(B_OUT, HIGH);
      break;

    case INDICATOR_GREEN:
      digitalWrite(R_OUT, LOW);
      digitalWrite(G_OUT, HIGH);
      digitalWrite(B_OUT, LOW);
      break;

    case INDICATOR_YELLOW:
      digitalWrite(R_OUT, HIGH);
      digitalWrite(G_OUT, HIGH);
      digitalWrite(B_OUT, LOW);
      break;

    case INDICATOR_WHITE:
      digitalWrite(R_OUT, HIGH);
      digitalWrite(G_OUT, HIGH);
      digitalWrite(B_OUT, HIGH);
      break;

    default:
        digitalWrite(R_OUT, LOW);
        digitalWrite(G_OUT, LOW);
        digitalWrite(B_OUT, LOW);
        break;
    }
}