from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt


def corrected_ec_2nd_order(ec, temp, a1=0.02, a2=0.0005, a3=0., a4=0., gfactor=1.0, reference=20.0 ):
    delta = temp - reference
    return gfactor*ec / (1 + a1*delta + a2*delta**2 + a3*delta**3 + a4*delta**4)

old_readings = [1.1725,  1.195,   1.2818,  1.36948, 1.5392,  1.53468, 1.32528] #these are raw, they come from calibrated: (with alpha = 0.02)np.array([1.25, 1.25, 1.30, 1.34, 1.48, 1.47, 1.32])
old_temps =  [16.9, 17.8, 19.3, 21.1, 22,   22.2, 20.2] 

# === Your input data here ===
# first entry is a fake one to make sure the function stays in range
temperatures =   [35,    18.9, 18.9, 18.1, 16.9, 15.7, 14.7, 13.8,  13.4, 13.8, 14.6, 14.6, 14.6, 10.0, 14.3, 14.6, 11.6,  7.8,  17.4, 15.5]  # in °C
ec_readings  =   [2.0,   1.2,  1.19, 1.13, 1.06, 1.00, 0.96, 0.91,  0.89, 0.89, 0.91, 0.91, 0.90, 0.76, 0.87, 0.86, 0.78,  0.7,  0.96, 0.89]  # in mS/cm (raw, uncorrected)
 
calib_readings = [1.1,   1.1,  1.09, 1.08, 1.08, 1.07, 1.07, 1.15,  1.15, 1.09, 1.12, 1.11, 1.10, 1.10, 1.07, 1.05, 1.03,  1.07, 1.09, 1.3, 1.15] # in mS/cm (calibrated)
#                                                                                                                   #guess,guess

times =          [None,  22,   0,    2,    4,    6,    8   , 10  ,  13,   14  , 16,   18  , 20  , 6   , 18,   16  , 1,     6,    16,   19,  14] #just for info, not used in the fit


target_ec = np.array(calib_readings) #*0. + 1.1

initial_guess = [0.05, 0.001, 0., 0., 1.]

fixed_parameters = None # [0.0594, 0.0085, 0.8387] # [a1, a2, gfactor]

# from old readings:  a1=0.0594, a2=0.0085, gfactor=0.8387
# from new readings:  a1=0.0591, a2=0.0030, gfactor=0.8600

# === input data end ===


def fit_func(X, a1, a2, a3, a4, gfactor):
    ec, temp = X
    # Apply the 2nd order polynomial correction
    return corrected_ec_2nd_order(ec, temp, a1, a2, a3, a4, gfactor)

# Prepare data for curve fitting
ec_readings_raw = np.array(ec_readings)
temperatures = np.array(temperatures)
# in tuple
X_data = (ec_readings_raw, temperatures)



if(fixed_parameters is not None):
    a1, a2, a3, g = fixed_parameters
else:
    popt, pcov = curve_fit(fit_func, X_data, target_ec, p0=initial_guess)
    a1, a2, a3, a4, g = popt
    print(f"\nFitted coefficients: a1={a1:.4f}, a2={a2:.6f}, a3={a3:.8f}, a4={a4:.8f}, gfactor={g:.4f}")
# Plot the fitted curve
plt.figure(figsize=(10, 6))
# plot the readings by index, including the calibrated ones and the calibration target
plt.plot(range(len(ec_readings)), ec_readings, 'o', label='Raw EC Readings')
#now the calibrated raw readings using the fitted coefficients
calibrated_ec = corrected_ec_2nd_order(ec_readings_raw, temperatures, a1, a2, a3, a4, g)
plt.plot(range(len(calibrated_ec)), calibrated_ec, 'o', label='Calibrated EC Readings')
plt.plot(range(len(calib_readings)), calib_readings, 'x', label='Calibration EC Readings')
#scale y axis to max-min+-10%
ecdelta = max(ec_readings[1:]) - min(ec_readings[1:])
#plt.ylim(min(ec_readings[1:])-0.1*ecdelta, max(ec_readings[1:])+0.1*ecdelta)

#plot the temperatures as text to the raw readings
for i, txt in enumerate(temperatures):
    plt.annotate(str(txt)+ "˚C", (i, ec_readings[i]), textcoords="offset points", xytext=(0,10), 
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
corrected_ec = corrected_ec_2nd_order(ec_val, temp_range, a1, a2, a3, a4, g)
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
plt.plot(temp_range, ec_val/(1+0.019*(temp_range-20.)), color='g', linestyle='--', label='Literature Correction Factor')
plt.ylim(0.5, 2)
plt.legend()
plt.grid()
plt.show()
