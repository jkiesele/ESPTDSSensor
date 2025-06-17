
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
        delay(1000);  // Stabilization time 
    }

     // Oversampling for stability
     float ADCValue = 0;
     EC = 1;
     for (int i = 0; i < EC_OVERSAMPLING; i++) {
        delay(30);//wait for ADC to stabilize
        int rawADC = adc1_get_raw((adc1_channel_t) digitalPinToAnalogChannel(adcPin));
        if (rawADC < 0 || rawADC > 4095) {
            gLogger->println("Error: ADC reading out of range!");
            digitalWrite(powerPin, LOW);
            EC = -1;  // Use NaN for invalid readings
            break;
        }
        ADCValue += rawADC;
     }
     ADCValue /= (float)EC_OVERSAMPLING;

     turnOffEC();

     if(EC >= 0){
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
    turnOnEC();
    updateTemperature();
    // Stabilization time for TDS sensor, shorter since we took time reading temperature
    delay(800); 
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
