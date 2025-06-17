#ifndef ECSensor_h
#define ECSensor_h

#include <Arduino.h>
#include <driver/adc.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <limits>  // For NaN values

#define EC_OVERSAMPLING 10

class ECSensor {
    
    /*
    Use pins powerPin and adcPin to interface with the TDS sensor.
    The temperature sensor is connected to the OneWire bus on temperaturePin.

    For ESP32, the ADC pin must be a pin that supports ADC1, which is pins 1-10 on the ESP32 S3.
    */
public:
    ECSensor(int powerPin, int adcPin, int temperaturePin) 
        : oneWire(temperaturePin), sensors(&oneWire), powerPin(powerPin), adcPin(adcPin) {}

    void begin();

    void updateEC();
    void updateTemperature();
    void update();

    // returns the last measured TDS value
    float getTDS() const { return EC/0.001428571429;; }
    float getEC() const {return EC;} // calibrate; this is what's actually measured 1/(0.7*1000) here
    float getRawTDS() const { return rawEC/0.001428571429; } // returns the last measured TDS value at reference temperature
    float getRawEC()const {return rawEC;} // calibrate; this is what's actually measured 1/(0.7*1000) here
    float getRawADC() const { return rawADC; } // returns the last measured ADC value
    // returns the last measured temperature value
    float getTemperature() { return temperature; }

    void setProbeGain(double gain);
    double getProbeGain() const { return probeGain; }

    void setSeriesEC(double seriesEC);
    double getSeriesEC() const { return seriesEC; }

private:
    static constexpr float REF_TEMP = 20.;  // Invalid temperature value
    OneWire oneWire;
    DallasTemperature sensors;
    int powerPin, adcPin;
    float temperature = -127;
    float EC = -1;
    float rawEC = -1;
    float rawADC = 0;
    double probeGain = 0.588055892647049; // Gain of the EC probe, can be adjusted based on calibration
    double seriesEC = 1.0 - 0.0911175171588055; // Series EC of the series resistor, adjust if needed

    void turnOnEC() { digitalWrite(powerPin, HIGH); }
    void turnOffEC() { digitalWrite(powerPin, LOW); }

    float ADCtoEC(float ADCValue, float temperature=REF_TEMP);
};

#endif