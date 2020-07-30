#ifndef _INDICATOR_LIGHT_H
#define _INDICATOR_LIGHT_H

# include <stdint.h>

//defines for indicator colors:
#define INDICATOR_OFF 0
#define INDICATOR_RED 1
#define INDICATOR_BLUE 2
#define INDICATOR_GREEN 3
#define INDICATOR_YELLOW 4

class IndicatorLight {
public:
//default constructor
IndicatorLight(uint8_t R_PIN, uint8_t G_PIN, uint8_t B_PIN);

void setColor(uint8_t color);
uint8_t getColor() {return currentColor;}
private:
uint8_t currentColor;
int rPin;
int gPin;
int bPin;
};

#endif