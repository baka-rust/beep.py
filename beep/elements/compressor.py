from beep.elements.audio_element import AudioElement


class Compressor(AudioElement):

    def __init__(self, inpt, amplitude=1):
        self.input = inpt
        self.amplitude = amplitude  # float between 0 and 1

    def gen_sample(self):
        return chr(int(self.input.gen_sample() * self.amplitude))
