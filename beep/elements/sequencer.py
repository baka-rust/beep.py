from beep.constants import SAMPLE_RATE, SAMPLER_RESOLUTION, BEATS_PER_MINUTE
from beep.elements.audio_element import AudioElement
from beep.elements.oscillator import Oscillator


class Sequencer(AudioElement):

    def __init__(self, sequence=[261.63], bpm=BEATS_PER_MINUTE):
        self.oscillator = Oscillator()
        self.bpm = bpm
        self.sequence = sequence
        self.sequence_index = 0
        self.sample_counter = 0

        beats_per_second = bpm / 60.0
        samples_per_beat = SAMPLE_RATE / beats_per_second
        self.samples_per_event = samples_per_beat / SAMPLER_RESOLUTION

        self.oscillator.set_freq(self.sequence[self.sequence_index])

    def gen_sample(self):
        self.sample_counter += 1
        if self.sample_counter > self.samples_per_event:
            # goto next event
            self.sample_counter = 0
            self.sequence_index = (self.sequence_index + 1) % len(self.sequence)
            self.oscillator.set_freq(self.sequence[self.sequence_index])

        return self.oscillator.gen_sample()
