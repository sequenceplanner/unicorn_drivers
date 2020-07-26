#include "src/Adafruit-VL530X/Adafruit_VL53L0X.h"
#include "TrashActuator.h"

// address we will assign if dual sensor is present
#define LOXR_ADDRESS 0x30
#define LOXF_ADDRESS 0x31
// last one will be left with default adress 0x29

// set the pins to shutdown
#define SHT_LOXR A3 //right 
#define SHT_LOXF 3 //front (diode connected)
#define SHT_LOXL 2 //left  (diode connected)

// set the pins for motor control
#define IN1 6
#define IN2 5

//define sensor states
#define LOX_OUT_OF_RANGE 4

// objects for the vl53l0x
Adafruit_VL53L0X loxRight = Adafruit_VL53L0X();
Adafruit_VL53L0X loxFront = Adafruit_VL53L0X();
Adafruit_VL53L0X loxLeft = Adafruit_VL53L0X();

/*
    Reset all sensors by setting all of their XSHUT pins low for delay(10), then set all XSHUT high to bring out of reset
    Keep sensor #1 awake by keeping XSHUT pin high
    Put all other sensors into shutdown by pulling XSHUT pins low
    Initialize sensor #1 with lox.begin(new_i2c_address) Pick any number but 0x29 and it must be under 0x7F. Going with 0x30 to 0x3F is probably OK.
    Keep sensor #1 awake, and now bring sensor #2 out of reset by setting its XSHUT pin high.
    Initialize sensor #2 with lox.begin(new_i2c_address) Pick any number but 0x29 and whatever you set the first sensor to
 */


//function prototypes:
void setID();
int readRange(Adafruit_VL53L0X *sensor);
void initActuator();
void setActuator(uint8_t mode);

void setup() {
  Serial.begin(115200);
  // wait until serial port opens for native USB devices:
  while (! Serial) { delay(1); }

  //configure adress for all 3 sensors:
  setID();
}

void loop() {

  //set up local variables;
  static int rightRange, leftRange, frontRange;
  static unsigned long timeInterval;

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