import numpy as np
import matplotlib.pyplot as plt

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

const = 30

mu, sig = 3.02, 0.05

x_range = np.linspace(0, 10, 100) + const
y_range = gaussian(x_range, mu + const, sig)
print y_range
y_log = np.log10(y_range)


print y_log
print

plt.plot(x_range, y_log)

plt.show()