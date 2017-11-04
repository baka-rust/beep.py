from beep.constants import SAMPLE_RATE
from beep.elements.audio_element import AudioElement


class Oscillator(AudioElement):

    def __init__(self):
        self.wavetable = bytearray(([255]*128) + ([0]*128))
        self.table_index = 0
        self.table_step_counter = 0

        self.set_freq(261.625565)  # middle c

    def set_freq(self, freq):
        self.freq = freq
        self.samples_per_sec = SAMPLE_RATE / self.freq
        self.table_step_rate = len(self.wavetable) / float(self.samples_per_sec)

    def gen_sample(self):
        self.table_step_counter = self.table_step_counter + self.table_step_rate
        table_index = int(self.table_step_counter) % len(self.wavetable)
        return self.wavetable[table_index]
