import matplotlib.pyplot as plt
import numpy as np
import time
import serial
import tkinter as tk
from tkinter import messagebox

# Set up the serial port to read from Arduino
ser = serial.Serial("COM3", 9600)

# Initialize lists to store time and temperature data
times = []
temperatures = []

# Start time for plotting and set a maximum number of data points
start_time = time.time()
max_data_points = 120  # Example: Collect data for about a minute (if every reading takes 1 second)
is_data_collection_done = False

# Create a real-time plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()

try:
    while True:
        # Read incoming temperature data
        data = ser.readline().decode().strip()
        
        # Convert temperature data to float
        try:
            temperature = float(data)  # Convert to float after stripping whitespace
        except ValueError:
            print(f"Invalid data received: {data}")
            continue  # Skip the rest of the loop if data is invalid

        # Get elapsed time
        current_time = time.time() - start_time
        
        # Append new data to lists
        times.append(current_time)
        temperatures.append(temperature)

        # Clear and update the plot
        ax.clear()
        ax.plot(times, temperatures, label='Temperature (°F)', color='blue')
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Temperature (°F)')
        ax.set_title('Live Temperature Monitoring')
        ax.legend()
        ax.grid()

        # Check if data collection is completed
        if len(times) >= max_data_points:
            is_data_collection_done = True
            break  # Exit loop after gathering enough data for a minute

        # Pause for a short interval before the next update
        plt.pause(0.1)

    # After data collection is done, check if the temperature is normal
    avg_temperature = np.mean(temperatures)
    
    # Create alert message based on the average temperature
    if avg_temperature < 97.0:
        health_status = "The person's temperature is below normal (hypothermia)."
    elif 97.0 <= avg_temperature <= 100.4:
        health_status = "The person's temperature is normal."
    else:
        health_status = "The person's temperature is above normal (possible fever)."

    # Create a Tkinter window for the message box
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Temperature Results", f"Average Temperature: {avg_temperature:.2f} °F\n{health_status}")

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    # Finalize the plot
    plt.ioff()  # Turn off interactive mode
    plt.show()  # Keep the final plot open
    ser.close()  # Close the serial connection

# Close the plot window
plt.close(fig)