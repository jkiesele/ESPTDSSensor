import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

"""
Measurements for EC calibration
Taken 7.6.2025
Using tomatoes_grow solution, double strength, then diluted with distilled water in steps as indicated below.

Taken with QCRobot sensor, with 502 Ohm resistor in series to the probe to extend the range of the ADC readings.
"""

# the readings beyond 2mS/cm seem less reliable, so we will not use them for the calibration
EC  = [    1.82, 1.60, 1.47, 1.35, 1.23, 1.14, 1.03, 0.895, 0.754, 0.674, 0.565, 0.372, 0.000] # 2.11, 1.97,3.90, 3.40,2.95,     2.56, 
T   = [    23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0, 23.0 , 23.0 , 22.9 , 23.0 , 23.0 , 23.0 ] # 23.0, 23.0,23.0, 23.0,23.0,     23.0, 
ADC = [    1021, 970 , 937 , 910,  871 , 840 , 806 , 755  , 692  , 645  , 580  , 450  , 0000]  # 1183, 1143,1460, 1415,1307,     1167, 


def ec_temp_correction(ec, temp, a1=0.019):
    REF_TEMP = 25.0
    return ec / (1 + a1*(temp-REF_TEMP)) #apply the temp correction factor

def adc_to_ec(adc, temp, a = 0.588055892647049, b = -0.0911175171588055, aa = 0.0):
    b = 1.0 + b
    ec_tot = a * adc / 1000. 
    ec = 1 / ( 1/ec_tot - 1/b)
    ec = ec_temp_correction(ec, temp)
    return ec

def fit_func(X, a, b, aa):
    adc, temp = X
    return adc_to_ec(adc, temp, a, b, aa)

# Prepare data for curve fitting
adc_readings_raw = np.array(ADC)
temperatures = np.array(T)
target_ec = np.array(EC)

# in tuple
X_data = (adc_readings_raw, temperatures)

# Perform curve fitting
popt, pcov = curve_fit(fit_func, X_data, target_ec, p0=[0.6890918312691577, .2, 0.], maxfev=10000)
a, b, aa = popt
print(f"Fitted parameters: a = {a}, b = {b}, aa = {aa}")
# Plot the fitted curve
plt.figure(figsize=(10, 6))
# Plot the readings by index, including the calibrated ones and the calibration target
# Now the calibrated raw readings using the fitted coefficients
calibrated_ec = adc_to_ec(adc_readings_raw, temperatures, a, b, aa)
plt.plot(adc_readings_raw, calibrated_ec, 'o', label='Calibrated EC Readings', markersize=8)
plt.plot(adc_readings_raw, target_ec, 'x', label='Target EC Readings', markersize=8)
#plot calibration curve
adc_range = np.linspace(min(adc_readings_raw), max(adc_readings_raw), 100)
corrected_ec = adc_to_ec(adc_range, np.mean(temperatures), a, b, aa)
plt.plot(adc_range, corrected_ec, label='Calibration Curve', color='orange')

plt.xlabel('ADC Readings')
plt.ylabel('EC (mS/cm)')
plt.title('EC Calibration Curve')
plt.legend()
plt.grid()
plt.show()

## now plot the difference between the calibrated and target EC readings
plt.figure(figsize=(10, 6))
# Calculate the difference between calibrated and target EC readings as a function of target EC
diff_ec = calibrated_ec - target_ec
plt.plot(target_ec, diff_ec, 'o-', label='Difference (Calibrated - Target)', markersize=8)
plt.axhline(0, color='red', linestyle='--', label='Zero Difference Line')
plt.xlabel('ADC Readings')
plt.ylabel('Difference in EC (mS/cm)')
plt.title('Difference Between Calibrated and Target EC Readings')
plt.legend()
plt.grid()
plt.show()


#plot the calbration curve with the fitted parameters
plt.figure(figsize=(10, 6))
adc_range = np.linspace(min(adc_readings_raw), max(adc_readings_raw), 100)
corrected_ec = adc_to_ec(adc_range, np.mean(temperatures), a, b, aa)
plt.plot(adc_range, corrected_ec, label='Corrected EC', color='blue')
ec_val = 1.0
plt.axhline(y=ec_val, color='red', linestyle='--', label='Raw EC')

#also plot the contribution of the quadratic term
quadratic_contribution = aa * (adc_range / 1000.)**2
plt.plot(adc_range, corrected_ec - quadratic_contribution, label='Linear Contribution', color='green', linestyle='--')
#and the linear contribution
linear_contribution = a * adc_range / 1000.
plt.plot(adc_range, linear_contribution, label='Linear Contribution', color='purple', linestyle='--')

plt.xlabel('ADC Readings')
plt.ylabel('EC (mS/cm)')
plt.title('EC Calibration Curve with Fitted Parameters')
plt.legend()
plt.grid()
plt.show()

#plot temperature correction factor as function of temperature
temp_range = np.linspace(5, 40, 100)
corrected_ec = adc_to_ec(1200., temp_range, a, b, aa)
plt.figure(figsize=(10, 6))
plt.plot(temp_range, corrected_ec, label='Corrected EC', color='blue')
ec_val = 1.0
plt.axvline(x= 25., color='red', linestyle='--', label='Reference EC')
plt.xlabel('Temperature (°C)')
plt.ylabel('Corrected EC (mS/cm)')
plt.title('Correction vs Temperature')
plt.legend()
plt.grid()
plt.show()

