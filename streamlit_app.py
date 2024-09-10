import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Create a function to generate the heart shape
def plot_heart(t):
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    return x, y

# Set up the Streamlit page
st.title('!<3U')

# Create a Streamlit plot
plot = st.pyplot(plt.figure())

# Time steps for the animation
t = np.linspace(0, 2 * np.pi, 100)

# Animate the heart shape
for i in range(1, len(t)):
    plt.clf()  # Clear the figure
    x, y = plot_heart(t[:i])  # Get the heart shape coordinates up to current step
    plt.plot(x, y, color='red')  # Plot the heart shape
    plt.xlim([-20, 20])  # Set x-axis limits
    plt.ylim([-20, 15])  # Set y-axis limits
    plot.pyplot(plt.gcf())  # Update the plot in Streamlit
    time.sleep(0.0001)  # Slow down the animation
