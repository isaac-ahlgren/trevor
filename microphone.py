import pyaudio
import numpy as np

class Microphone:
    def __init__(self, sample_rate, buffer_size):
        self.format = pyaudio.paFloat32
        self.sample_rate = sample_rate
        self.pyaud = pyaudio.PyAudio()
        self.buffer_size = buffer_size
        self.stream = self.pyaud.open(format=self.format,
                                  channels=1,
                                  rate=sample_rate,
                                  input=True,
                                  frames_per_buffer=buffer_size)

    def get_audio(self):
        buf = self.stream.read(self.buffer_size)
        return np.fromstring(buf, dtype=np.float32)