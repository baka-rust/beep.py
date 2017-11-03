from beep.constants import SAMPLE_RATE
from beep.elements.audio_element import AudioElement


class Oscillator(AudioElement):

    def __init__(self):
        self.wavetable = bytearray(([255]*128) + ([0]*128))
        self.table_index = 0

        self.set_freq(261.625565)  # middle c

    def set_freq(self, freq):
        self.freq = freq
        self.samples_per_sec = SAMPLE_RATE / self.freq
        self.table_step_rate = len(self.wavetable) / self.samples_per_sec

    def gen_sample(self):
        self.table_index = int(self.table_index + self.table_step_rate) % len(self.wavetable)
        return self.wavetable[self.table_index]
