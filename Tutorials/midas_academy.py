import numpy as np
import matplotlib.pyplot as plt

import lime


fig_cfg = {'figure.figsize': (12, 6),
           'figure.dpi': 300, "axes.titlesize": 16, "axes.labelsize": 20,
           "legend.fontsize" : 16}

lime.theme.set_style('dark')


def generate_white_noise(sample_rate):
    """
    Generates white noise.

    Parameters:
    duration (float): Duration of the noise in seconds.
    sample_rate (int): Number of samples per second.

    Returns:
    numpy.ndarray: Array of white noise samples.
    """
    white_noise = np.random.normal(0.1, 0.025, sample_rate)
    return white_noise

# Parameters
sample_rate = 8000  # samples per second (standard for audio)

# Generate white noise
noise = generate_white_noise(sample_rate)

# Plot the white noise
plt.figure(figsize=(10, 4))
plt.plot(noise, color='blue')
plt.title("White Noise")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.show()