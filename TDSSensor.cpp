
#include <TDSSensor.h>

void TDSSensor::begin() {
        sensors.begin();
        pinMode(powerPin, OUTPUT);
        pinMode(adcPin, INPUT);

        // ADC Configuration
        adc1_config_width(ADC_WIDTH_BIT_12);
        adc1_config_channel_atten((adc1_channel_t) digitalPinToAnalogChannel(adcPin), ADC_ATTEN_DB_12);
    }

 void TDSSensor::updateTDS(bool turnOn, float& ADCValue) {
    if(turnOn){
        turnOnTDS();
        delay(500);  // Stabilization time for amplifier
    }

     // Oversampling for stability
     //float ADCValue = 0;
     for (int i = 0; i < TDS_OVERSAMPLING; i++) {
         int rawADC = adc1_get_raw((adc1_channel_t) digitalPinToAnalogChannel(adcPin));
         if (rawADC < 0 || rawADC > 4095) {
             digitalWrite(powerPin, LOW);
             TDS = -1;  // Use NaN for invalid readings
             return;
         }
         ADCValue += rawADC;
         delayMicroseconds(5000);
     }
     ADCValue /= (float)TDS_OVERSAMPLING;

     digitalWrite(powerPin, LOW);  // Turn off sensor

     TDS = ADCtoTDS(ADCValue, temperature);
 }

void TDSSensor::updateTemperature(){
    sensors.requestTemperatures();
    temperature = sensors.getTempCByIndex(0);

    if (temperature == DEVICE_DISCONNECTED_C) {  
         temperature = -127;  // Mark as invalid
    }
}

void TDSSensor::update(float& adcval) {
    turnOnTDS();
    updateTemperature();
    // Stabilization time for TDS sensor, shorter since we took time reading temperature
    delay(300); 
    updateTDS(false,adcval);
}

 float TDSSensor::ADCtoTDS(float ADCValue, float temperature) {
    //return ADCValue;
     if (temperature < -100) temperature = 20.0;  // Assume room temp if invalid
     /* calibration logic goes here */
     // [0.34770145 0.02302332 0.00440754]
     float calibrated = 0.34770145*ADCValue + 0.02302332* (exp( 0.00440754*ADCValue) - 1.);
     if(calibrated < 0) calibrated = -0.001;
     return calibrateTDStoTemperature(calibrated,temperature);
}

float TDSSensor::calibrateTDStoTemperature(float TDS, float temperature) {
        const float tempCalibration = 0.02;  // Calibration factor for temperature
        const float referenceTemp = 20.0;    // Reference temperature for calibration
        float out = TDS / (1.0 + tempCalibration * (temperature - referenceTemp));
        if(out < 0) out = -0.001;
        return out;
}