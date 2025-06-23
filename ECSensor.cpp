
#include <ECSensor.h>
#include <cmath>
#include <algorithm> 
#include "LoggingBase.h"

void ECSensor::begin() {
        sensors.begin();
        pinMode(powerPin, OUTPUT);
        pinMode(adcPin, INPUT);

        // ADC Configuration
        adc1_config_width(ADC_WIDTH_BIT_12);
        adc1_config_channel_atten((adc1_channel_t) digitalPinToAnalogChannel(adcPin), ADC_ATTEN_DB_12);

        Serial.println("TDS Sensor Initialized");
    }

 void ECSensor::updateEC() {
    //check if turned on
    if(digitalRead(powerPin) == LOW){
        turnOnEC();
        delay(600);  // Stabilization time 
    }

     // Oversampling for stability
     float ADCValue = 0;
     EC = 1;
     for (int i = 0; i < EC_OVERSAMPLING; i++) {
        delay(10);//wait for ADC to stabilize
        int thisADC = adc1_get_raw((adc1_channel_t) digitalPinToAnalogChannel(adcPin));
        if (thisADC < 0 || thisADC > 4095) {
            gLogger->println("Error: ADC reading out of range!");
            EC = -1;  // Use NaN for invalid readings
            break;
        }
        ADCValue += thisADC;
     }
     

     turnOffEC();

     if(EC >= 0){
        ADCValue /= (float)EC_OVERSAMPLING;
        EC = ADCtoEC(ADCValue, temperature);
        rawEC = ADCtoEC(ADCValue);//at reference temperature
        rawADC = ADCValue;  // Store raw ADC value
     }
    else{
        EC = -1;  // Use NaN for invalid readings
        rawEC = -1;
        rawADC = -1;
    }
 }

void ECSensor::updateTemperature(){
    sensors.requestTemperatures();
    temperature = sensors.getTempCByIndex(0);

    if (temperature == DEVICE_DISCONNECTED_C) {  // Clearly invalid for water
         gLogger->println("Error: DS18B20 temperature sensor not detected or faulty!");
         temperature = -127;  // Mark as invalid
    }
}

void ECSensor::update() {
    uint32_t startTime = millis();
    turnOnEC();
    updateTemperature();
    // Stabilization time for TDS sensor, shorter since we took time reading temperature
    uint32_t stabilizationTime = 600 - (millis() - startTime);
    delay(stabilizationTime > 0 ? stabilizationTime : 0);  // Ensure we don't delay negative time
    updateEC();
}

void ECSensor::setProbeGain(double gain) {
    if (gain > 0) {
        probeGain = gain;
    } else {
        gLogger->println("Invalid gain value. Gain must be positive.");
    }
}

void ECSensor::setSeriesEC(double seriesEC) {
    if (seriesEC > 0) {
        this->seriesEC = seriesEC;
    } else {
        gLogger->println("Invalid series EC value. Series EC must be positive.");
    }
}

static inline double ec_temp_correction(double ec, double temp, double a1) {
    return ec / (1.0 + a1 * (temp - 25.0));
}

float ECSensor::ADCtoEC(float adc, float temp) {

    // series EC of the series resistor 
    double b = seriesEC;
    double a = probeGain; // for std sensor gain should be one

    double ec_tot = a * adc / 1000.;
    double ec = 1 / ( 1/ec_tot - 1/b);
    ec = ec_temp_correction(ec, static_cast<double>(temp), 0.019);
    return static_cast<float>(ec);
}
