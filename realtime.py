import serial
import matplotlib.pyplot as plt
from collections import deque
import numpy as np

# Serial port settings
serial_port = 'COM1'  # Update this with the correct port for your Arduino
baud_rate = 115200

# Time window for plotting (in seconds)
time_window = 10

# Initialize lists for time and current values
time_values = list()  # Assuming 1000 samples per second
current_values = list()

# Initialize energy calculation variables
energy_values = list()
energy_values.append(0)
last_time = 0
total_energy = 0

# Calibration values
corr_a=1.2393985838010886
corr_b=1
corr_c=-9.388948900526534

voltage = 5.0  # Voltage used for calibration

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1)
plt.ion()  # Turn on interactive mode for real-time plotting

# Open serial connection
#ser = serial.Serial(serial_port, baud_rate)

try:
    while True:
        # Read data from serial port
        #raw_value = float(ser.readline().decode().strip()) / 10.24
        raw_value = float(np.random.rand())
        # Convert raw value to current
        calibrated_value = raw_value**(1 / corr_b) / corr_a - corr_c
        
        # Update time and current values
        current_time = len(time_values) / 1000  # Time in seconds
        current_values.append(calibrated_value)
        time_values.append(current_time)

        # Calculate energy using trapezoidal rule
        if last_time != 0:
            dt = current_time - last_time
            energy = voltage * ((current_values[-1] + current_values[-2]) / 1000) * dt
            total_energy += energy
            energy_values.append(total_energy)

        # Trim lists to only keep the last 10 seconds of data
        time_values = time_values[-int(time_window * 1000):]
        current_values = current_values[-int(time_window * 1000):]
        energy_values = energy_values[-int(time_window * 1000):]

        # Update plots
        ax1.clear()
        ax1.plot(time_values, current_values, label='Current (A)')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Current (A)')
        ax1.legend()

        ax2.clear()
        ax2.plot(list(time_values)[-len(energy_values):], list(energy_values), label='Total Energy (J)')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Total Energy (J)')
        ax2.legend()

        plt.pause(0.001)

        last_time = current_time

        print(current_time, len(time_values), len(current_values), len(energy_values))

except KeyboardInterrupt:
    # Close the serial port on keyboard interrupt
    #ser.close()
    print("Serial port closed.")

# Keep the plots open after the script finishes
plt.ioff()
plt.show()