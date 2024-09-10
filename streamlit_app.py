import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Interactive sliders
iterations = st.sidebar.slider("Animation Frames", 50, 200, 100, 10)
speed = st.sidebar.slider("Speed of animation (lower is faster)", 0.001, 0.1, 0.05)

# Non-interactive elements
progress_bar = st.sidebar.progress(0)
frame_text = st.sidebar.empty()
image = st.empty()

# Heart shape parametric equations
def heart_shape(t):
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    return x, y

# 3D rotation function
def rotate_3d(x, y, angle):
    """ Apply 3D rotation by projecting onto the xy-plane. """
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    
    # Rotate the heart in 3D space
    x_3d = cos_a * x - sin_a * y
    y_3d = sin_a * x + cos_a * y
    
    # Simulate perspective scaling (3D depth effect)
    scale = 0.7 + 0.3 * np.cos(angle)  # Adjust scaling for 3D depth perception
    return scale * x_3d, scale * y_3d

# Animate the heart shape
for frame_num, a in enumerate(np.linspace(0, 2 * np.pi, iterations)):
    progress_bar.progress(frame_num / iterations)
    frame_text.text(f"Frame {frame_num+1}/{iterations}")

    # Generate heart shape points
    t = np.linspace(0, 2 * np.pi, 1000)
    x_heart, y_heart = heart_shape(t)

    # Apply 3D rotation
    x_heart_3d, y_heart_3d = rotate_3d(x_heart, y_heart, a)

    # Create a plot and display the 3D rotated heart shape
    plt.figure(figsize=(6, 6))
    plt.plot(x_heart_3d, y_heart_3d, color='red')
    plt.xlim([-20, 20])
    plt.ylim([-20, 20])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')  # Turn off the axis

    # Update the image in the Streamlit app
    image.pyplot(plt.gcf())
    plt.close()

    time.sleep(speed)  # Use slider value for speed control

# Clear elements
progress_bar.empty()
frame_text.empty()

# Re-run button to trigger rerun manually
st.button("Re-run")
