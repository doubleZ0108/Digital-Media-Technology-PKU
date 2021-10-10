import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('data.csv')
x = np.array(data.loc[:, 'Bit rate(kbit/s)'])
y = np.array(data.loc[:, 'SNR Y(dB)'])
u = np.array(data.loc[:, 'SNR U(dB)'])
v = np.array(data.loc[:, 'SNR V(dB)'])

plt.plot(x, y, label='Y')
plt.plot(x, u, label='U')
plt.plot(x, v, label='V')

plt.scatter(x, y, c='black', marker='o')
plt.scatter(x, u, c='blue', marker='s')
plt.scatter(x, v, c='red', marker='^')

plt.title('Rate-Distortion Curce')
plt.xlabel('Bit rate(kbit/s)')
plt.ylabel('PSNR(dB)')

plt.grid(linestyle='-.')
plt.legend(loc='best')

plt.show()