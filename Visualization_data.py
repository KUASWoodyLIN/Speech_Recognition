import os
from os.path import isdir, join
from pathlib import Path
import pandas as pd

# Math
import numpy as np
from scipy.fftpack import fft
from scipy import signal
from scipy.io import wavfile
# import librosa

from sklearn.decomposition import PCA

# Visualization
import matplotlib.pyplot as plt
# import seaborn as sns
# import IPython.display as ipd
# import librosa.display

# import plotly.offline as py
# py.init_notebook_mode(connected=True)
# import plotly.graph_objs as go
# import plotly.tools as tls
# import pandas as pd

# %matplotlib inline

import tensorflow as tf

path, _ = os.path.split(os.path.abspath(__file__))
train_audio_path = path + '/train data/train/audio/'
filename = '/yes/0f7dc557_nohash_1.wav'
sample_rate, samples = wavfile.read(str(train_audio_path) + filename)


def log_specgram(audio, sample_rate, window_size=20,
                 step_size=10, eps=1e-10):
  nperseg = int(round(window_size * sample_rate / 1e3))
  noverlap = int(round(step_size * sample_rate / 1e3))
  freqs, times, spec = signal.spectrogram(audio,
                                          fs=sample_rate,
                                          window='hann',
                                          nperseg=nperseg,
                                          noverlap=noverlap,
                                          detrend=False)
  return freqs, times, np.log(spec.astype(np.float32) + eps)


def log_specgram2(audio, sample_rate, window_size=20,
                  step_size=10, eps=1e-10):
  nperseg = int(round(window_size * sample_rate / 1e3))
  noverlap = int(round(step_size * sample_rate / 1e3))
  freqs, times, spec = signal.stft(audio,
                                   sample_rate,
                                   nperseg=nperseg,
                                   noverlap=noverlap,
                                   nfft=512,
                                   padded=False,
                                   boundary=None)

  return freqs, times, np.log(spec.astype(np.float32) + eps)


freqs, times, spectrogram = log_specgram(samples, sample_rate)

fig = plt.figure(figsize=(14, 8))
ax1 = fig.add_subplot(211)
ax1.set_title('Raw wave of ' + filename)
ax1.set_ylabel('Amplitude')
ax1.plot(np.linspace(0, sample_rate/len(samples), sample_rate), samples)


ax2 = fig.add_subplot(212)
ax2.imshow(spectrogram, aspect='auto', origin='lower',
           extent=[times.min(), times.max(), freqs.min(), freqs.max()])
ax2.set_yticks(freqs[::16])
ax2.set_xticks(times[::16])
ax2.set_title('Spectrogram of ' + filename)
ax2.set_ylabel('Freqs in Hz')
ax2.set_xlabel('Seconds')

# plt.pcolormesh(times, freqs, spectrogram)
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')

plt.show()

