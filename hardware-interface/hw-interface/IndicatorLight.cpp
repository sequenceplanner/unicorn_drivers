#include "IndicatorLight.h"
#include "Arduino.h"

IndicatorLight::IndicatorLight(uint8_t R_PIN, uint8_t G_PIN, uint8_t B_PIN) {
    //rPin = R_PIN;
    //gPin = G_PIN;
    //bPin = B_PIN;
    rPin = 8;
    gPin = 9;
    bPin = 10;
    pinMode(R_PIN, OUTPUT);
    pinMode(G_PIN, OUTPUT);
    pinMode(B_PIN, OUTPUT);

    digitalWrite(R_PIN, LOW);
    digitalWrite(G_PIN, LOW);
    digitalWrite(B_PIN, LOW);

    currentColor = INDICATOR_OFF;
}

void IndicatorLight::setColor(uint8_t color) {
    Serial.println(F("Setting color"));
    Serial.println(rPin);
    Serial.println(gPin);
    Serial.println(bPin);

    switch (color) {
    case INDICATOR_OFF:
        digitalWrite(rPin, LOW);
        digitalWrite(gPin, LOW);
        digitalWrite(bPin, LOW);
        break;

    case INDICATOR_RED:
        digitalWrite(rPin, HIGH);
        digitalWrite(gPin, LOW);
        digitalWrite(bPin, LOW);
        break;

    case INDICATOR_BLUE:
        digitalWrite(rPin, LOW);
        digitalWrite(gPin, LOW);
        digitalWrite(bPin, HIGH);
        break;

    case INDICATOR_GREEN:
        digitalWrite(rPin, LOW);
        digitalWrite(gPin, HIGH);
        digitalWrite(bPin, LOW);
        break;

    case INDICATOR_YELLOW:
        digitalWrite(rPin, LOW);
        digitalWrite(gPin, HIGH);
        digitalWrite(bPin, HIGH);
        break;
    default:
        digitalWrite(rPin, LOW);
        digitalWrite(gPin, LOW);
        digitalWrite(bPin, LOW);
        break;
    }
}