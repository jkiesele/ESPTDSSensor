
#include <ECSensor.h>
#include <cmath>
#include <algorithm> 

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
            webLog.addToLog("Error: ADC reading out of range!");
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
         webLog.addToLog("Error: DS18B20 temperature sensor not detected or faulty!");
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

static inline double ec_temp_correction(double ec, double temp, double a1) {
    return ec / (1.0 + a1 * (temp - 25.0));
}

float ECSensor::ADCtoEC(float ADCValue, float temp) {
    constexpr double adc0 = 0.0005158386900113605;
    constexpr double adc1 = 6.622970656294487e-25;
    constexpr double adc2 = 19.409747146224944;
    constexpr double a1   = 0.019;

    double adc = ADCValue;
    double temperature = temp;

    // Linear part
    double ec = adc0 * adc;

    // Exponential part, safely clipped
    double exp_arg = adc2 * (adc / 1000.0);
    //safety
    if(exp_arg<-700) exp_arg = -700;
    if(exp_arg>700) exp_arg = 700;
    double exp_part = adc1 * (std::exp(exp_arg) - 1.0);

    // Switch to linear‐fallback above ADC ≈ 2857
    constexpr double linear_slope = (2.5 - 2.3) / (2867.0 - 2857.0);
    if (adc > 2857) {
        // linear interp between (2857, 2.3) and (2867, 2.5)
        ec = linear_slope * (adc - 2857) + 2.3;
    } else {
        ec += exp_part;
    }

    // Temperature correction
    double corr = ec_temp_correction(ec, temp, a1);
    return static_cast<float>(corr);
}
