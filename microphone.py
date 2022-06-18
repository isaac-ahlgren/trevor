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
        self.stream.start_stream()
        self.count = 0

    def get_audio(self):
        buf = self.stream.read(self.buffer_size, exception_on_overflow=False)
        decoded_buf = np.fromstring(buf, dtype=np.float32)
        #np.save("./pickled/test_audio_" + str(self.count) + ".npy", decoded_buf)
        #self.count += 1
        return decoded_buf
