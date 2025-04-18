#ifndef TDSSensor_h
#define TDSSensor_h

#include <Arduino.h>
#include <driver/adc.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <limits>  // For NaN values

#define TDS_OVERSAMPLING 10

class TDSSensor {
    
    /*
    Use pins powerPin and adcPin to interface with the TDS sensor.
    The temperature sensor is connected to the OneWire bus on temperaturePin.

    For ESP32, the ADC pin must be a pin that supports ADC1, which is pins 1-10 on the ESP32 S3.
    */
public:
    TDSSensor(int powerPin, int adcPin, int temperaturePin) 
        : oneWire(temperaturePin), sensors(&oneWire), powerPin(powerPin), adcPin(adcPin) {}

    void begin();

    void updateTDS(bool turnOn ,  float& ADCValue);
    void updateTemperature();
    void update(float& ADCValue);
    void update(){float dummy; update(dummy);}//overload

    // returns the last measured TDS value
    float getTDS() { return TDS; }
    float getEC(){return TDS*0.001428571429;} // calibrate; this is what's actually measured 1/(0.7*1000) here

    // returns the last measured temperature value
    float getTemperature() { return temperature; }

private:
    OneWire oneWire;
    DallasTemperature sensors;
    int powerPin, adcPin;
    float temperature = -127;
    float TDS = -1;
    float adcValue = 0;

    void turnOnTDS() { digitalWrite(powerPin, HIGH); }

    float ADCtoTDS(float ADCValue, float temperature);
    float calibrateTDStoTemperature(float TDS, float temperature);
};

#endif