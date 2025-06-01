from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import math


values = [1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.19, 1.18, 1.15, 1.17, 1.18, 1.18, 1.19, 1.19, 1.19, 1.20, 1.18, 1.17, 1.16, 1.15, 1.17, 1.17, 1.18, 1.19, 1.19, 1.19, 1.19, 1.19, 1.19, 1.19, 1.18, 1.14, 1.09, 1.06, 1.05, 1.04]
rawValues = [1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1924.70, 1930.40, 1960.40, 1963.40, 1980.80, 1998.30, 2005.40, 2001.20, 1988.80, 1976.10, 1972.90, 1933.20, 1906.90, 1892.90, 1849.50, 1824.50, 1792.50, 1768.10, 1740.20, 1704.60, 1678.50, 1650.20, 1630.50, 1624.30, 1684.70, 1774.00, 1875.20, 1941.00, 2007.40, 2028.70, 2029.20]
temps = [16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 16.75, 17.37, 17.87, 17.87, 18.12, 18.25, 18.06, 17.81, 17.62, 17.44, 17.00, 16.69, 16.50, 15.94, 15.25, 14.63, 14.06, 13.38, 12.63, 12.00, 11.31, 10.81, 10.69, 12.06, 14.19, 16.50, 18.31, 19.81, 20.44, 20.56]
#espTemps = [33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 34.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 33.50, 39.50, 40.50, 42.50, 41.50, 38.50, 38.50, 35.50, 34.50, 35.50, 35.50, 32.50, 33.50, 32.50, 30.50, 28.50, 28.50, 27.50, 26.50, 25.50, 25.50, 24.50, 24.50, 26.50, 31.50, 37.50, 40.50, 43.50, 47.50, 45.50, 46.50]

#cut all but the last 30 values
values = values[-30:]
rawValues = rawValues[-30:]
temps = temps[-30:]
#espTemps = espTemps[-30:] #not used atm
target_ec = (np.array(values) *0. + 1.15).tolist()

# now new by-hand measurements                                                                                |calibration applied here
values +=    [0.11, 0.14, 0.25,  0.35,  0.39,  0.47 , 0.56 , 0.67,  0.82,  1.05 , 1.40 , 2.44, 6.38,  7.47       2.01,   1.63, ] # just for reference
rawValues += [340,  420,  724,   1005,  1150,  1357 , 1572 , 1793,  1981,  2155 , 2309 , 2524, 2804,  2844 ,     2828,   2762, ] #2847
temps +=     [23.5, 23.5, 23.44, 23.44, 23.44, 23.31, 23.31, 23.25, 23.19, 23.12, 23.12, 23.0, 22.94, 22.87,     22.56,  22.56,]
target_ec += [0.17, 0.21, 0.356, 0.548, 0.635, 0.720, 0.880, 1.00,  1.11,  1.23 , 1.33 , 1.46, 1.80,  2.18,      1.97,   1.72, ]



def ec_temp_correction(ec, temp, a1=0.019):
    REF_TEMP = 25.0
    return ec / (1 + a1*(temp-REF_TEMP)) #apply the temp correction factor

# now the ADC reading is not necessarily linear - only up to a point; up to about 1800 (roughly EC of 1.2) counts it's linear.
# after that it becomes exponential, so we need to fit a curve to the data.
def adc_to_ec(adc, temp, adc0=0.0005158386900113605, adc1=6.622970656294487e-25, adc2=19.409747146224944, a1=0.019):
    ec =   adc0 * adc #work with this. starting from 1.2 it will get exp 
    exp = np.clip(adc2 * (adc / 1000.), -400, 400)
    exp_part = adc1 * (np.exp(exp) - 1.)
    # if adc is above 2870, just go linear again; a regime where we don't care too much anymore to avoid overshoots
    
    ec = np.where(adc > 2857, (2.5-2.3) / (2867-2857) * (adc - 2857) + 2.3, ec+exp_part)
    
    ec = ec_temp_correction(ec, temp, a1) #apply the temp correction factor
    return ec

def ec_to_ec25(ec, temp, a1=0.019):
    REF_TEMP = 25.0
    return ec * (1 + a1*(temp-REF_TEMP)) #apply the temp correction factor

initial_guess = [5e-4, 1e-5, 1e-4]#, 0.019] # [adc0, adc1, adc2, a1]
a1 = 0.019#fix to literature

fixed_parameters = None # [0.0594, 0.0085, 0.8387] # [a1, a2, gfactor]

# from old readings:  a1=0.0594, a2=0.0085, gfactor=0.8387
# from new readings:  a1=0.0591, a2=0.0030, gfactor=0.8600

# === input data end ===


def fit_func(X, adc0, adc1, adc2):
    adc, temp = X
    # Apply the 2nd order polynomial correction
    return adc_to_ec(adc, temp,adc0, adc1, adc2)

# Prepare data for curve fitting
adc_readings_raw = np.array(rawValues)
temperatures = np.array(temps)
target_ec = np.array(target_ec)
# in tuple
X_data = (adc_readings_raw, temperatures)



if(fixed_parameters is not None):
    adc0, adc1, adc2, a1 = fixed_parameters
else:
    popt, pcov = curve_fit(fit_func, X_data, target_ec, p0=initial_guess, maxfev=10000)
    adc0, adc1, adc2 = popt
    print(f"\nFitted coefficients: adc0={adc0}, adc1={adc1}, adc2={adc2}, a1={a1}")
# Plot the fitted curve
plt.figure(figsize=(10, 6))
# plot the readings by index, including the calibrated ones and the calibration target
plt.plot(range(len(adc_readings_raw)), adc_readings_raw/2000, 'o', label='Raw EC Readings')
#now the calibrated raw readings using the fitted coefficients
calibrated_ec = adc_to_ec(adc_readings_raw, temperatures, adc0, adc1, adc2, a1)
plt.plot(range(len(calibrated_ec)), calibrated_ec, 'o', label='Calibrated EC Readings')
plt.plot(range(len(target_ec)), target_ec, 'x', label='Calibration EC Readings')
#scale y axis to max-min+-10%
#plot the temperatures as text to the raw readings
for i, txt in enumerate(temperatures):
    plt.annotate(str(txt)+ "˚C", (i, adc_readings_raw[i]/2000), textcoords="offset points", xytext=(0,10), 
                 ha='center')
    
#now plot the temperature for each point on a second y axis
ax2 = plt.gca().twinx()
ax2.set_ylabel('Temperature (°C)')
ax2.plot(range(len(temperatures)), temperatures, 'r-', label='Temperature', alpha=0.5)
delta_temp = max(temperatures[1:]) - min(temperatures[1:])
#ax2.set_ylim(min(temperatures[1:])-0.1*delta_temp, max(temperatures[1:])+0.1*delta_temp)

plt.legend()
plt.grid()
plt.show()


#now plot the fitted correciton factor as function of temperature
#for temps between 5 and 35 C

temp_range = np.linspace(5, 35, 100)
ec_val = 1.0
corrected_ec = adc_to_ec(2000., temp_range,adc0, adc1, adc2, a1)
plt.figure(figsize=(10, 6))
plt.plot(temp_range, corrected_ec, label='Corrected EC')
plt.axhline(y=ec_val, color='r', linestyle='--', label='Raw EC')
plt.xlabel('Temperature (°C)')
plt.ylabel('Correction factor')
plt.title('Correction vs Temperature')
#plot also for only the LO coefficient
#plt.plot(temp_range, corrected_ec_2nd_order(ec_val, temp_range, a1, 0., 0., g), label='Corrected EC (a2=0, a3=0)')
#set y range to 0.5 to 2
#now also put the litarature correction factor
plt.plot(temp_range, ec_temp_correction(ec_val, temp_range), color='g', linestyle='--', label='Literature Correction Factor')
plt.ylim(0.5, 2)
plt.legend()
plt.grid()
plt.show()

#plot ec versus adc reading for fixed temp=20
temp = 25
adc_range = np.linspace(0, np.max(adc_readings_raw)+100, 100)
ec_range = adc_to_ec(adc_range, temp, adc0, adc1, adc2, a1)
plt.figure(figsize=(10, 6))
plt.plot(adc_range, ec_range, label='Corrected EC')
#also plot the raw values at 
#plt.axhline(y=ec_val, color='r', linestyle='--', label='Raw EC')

#shift the calibrated EC values to a temp of 20C
calibrated_ec_25 = adc_to_ec(adc_readings_raw, temperatures, adc0, adc1, adc2, a1)
#now move them as if they were at 20C (un-correct the temp)
calibrated_ec_25 = ec_to_ec25(calibrated_ec_25, temperatures, a1)
plt.plot(adc_readings_raw, calibrated_ec_25, 'o', label='Calibrated EC @ 20C')

plt.xlabel('ADC Reading')
plt.ylabel('EC (mS/cm)')
plt.title('EC vs ADC Reading')
plt.legend()
plt.grid()
plt.show()


#now plot the ratio of the adc correction curve and the measured values
plt.figure(figsize=(10, 6))
plt.plot(adc_readings_raw, (calibrated_ec_25/ec_to_ec25(target_ec, temperatures, a1)-1)*100, 'x', label='Calibrated EC @ 20C')
plt.axhline(y=1., color='r', linestyle='--', label='Calibration EC @ 20C')
plt.xlabel('ADC Reading')
plt.ylabel('Bias [%]')
plt.title('Correction vs ADC Reading')
plt.legend()
plt.grid()
plt.show()


# now plot the absolute error of calibrated ec versus target ec for all points
# first, as a function of the raw adc reading
# second, as a function of the temperature
plt.figure(figsize=(10, 6))
plt.plot(adc_readings_raw, (calibrated_ec-target_ec), 'x', label='Calibrated EC @ 20C')
plt.axhline(y=0., color='r', linestyle='--', label='Calibration EC @ 20C')
plt.xlabel('ADC Reading')
plt.ylabel('Absolute Error [mS/cm]')
plt.title('Absolute Error vs ADC Reading')
plt.legend()
plt.grid()
plt.show()

# now plot the absolute error of calibrated ec versus target ec for all points
plt.figure(figsize=(10, 6))
plt.plot(temperatures, (calibrated_ec-target_ec), 'x', label='Calibrated EC @ 20C')
plt.axhline(y=0., color='r', linestyle='--', label='Calibration EC @ 20C')
plt.xlabel('Temperature [°C]')
plt.ylabel('Absolute Error [mS/cm]')
plt.title('Absolute Error vs Temperature')
plt.legend()
plt.grid()
plt.show()

