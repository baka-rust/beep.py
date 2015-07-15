# audio generation with 8bit wav
# has synth stuff like Wave-table Oscillators, Mixers, Compressors, Sequencers, Samplers, etc

import wave
import math

SAMPLE_RATE = 44100


#TODO: envelopes, sampler (sample sequencer)

class Signal:

    def __init__(self):
        self.char = chr(127)

    def send(self, byte):
        self.char = byte

    def poll(self):
        return self.char


class Oscillator:

    def __init__(self, freq):
        self.freq = freq
        self.wavetable = []
        self.samples_per_cycle = SAMPLE_RATE / freq
        self.dt = 0

        self.output = Signal()

        self.set_wavetable_sin()

    def set_freq(self, freq):
        self.freq = freq
        self.samples_per_cycle = SAMPLE_RATE / freq
        self.update_cycle = float(len(self.wavetable)) / float(self.samples_per_cycle)

    def set_wavetable(self, wavetable):
        self.wavetable = wavetable
        self.update_cycle = float(len(self.wavetable)) / float(self.samples_per_cycle)

    def set_wavetable_sin(self, sample_length=256):
        phase_increment = (2 * math.pi) / sample_length
        current_phase = 0.0

        self.wavetable = []
        for i in range(0, sample_length):
            self.wavetable.append(int((math.sin(current_phase) * 127) + 127))
            current_phase += phase_increment
        self.update_cycle = float(len(self.wavetable)) / float(self.samples_per_cycle)

    def set_wavetable_saw(self, sample_length=256):
        self.wavetable = []
        for i in range(0, sample_length):
            self.wavetable.append(int((255.0 / sample_length) * i))
        self.update_cycle = float(len(self.wavetable)) / float(self.samples_per_cycle)

    def set_wavetable_square(self, sample_length=256):
        self.wavetable = []
        for i in range(0, sample_length):
            if i < (sample_length/2):
                self.wavetable.append(0)
            else:
                self.wavetable.append(255)
        self.update_cycle = float(len(self.wavetable)) / float(self.samples_per_cycle)

    def generate_frame(self):
        b = self.wavetable[int(self.dt) % len(self.wavetable)]
        self.dt += self.update_cycle
        self.output.send(chr(b))


class Mixer:

    def __init__(self, *signals):
        self.signals = []
        self.output = Signal()

        for signal in signals:
            self.signals.append(signal)

    def add_signal(self, signal):
        self.signals.append(signal)

    def generate_frame(self):
        total = 0
        for signal in self.signals:
            total += ord(signal.poll())
        total = total / len(self.signals)
        self.output.send(chr(total))


class Sequencer:

    def __init__(self, bpm=80, sequence=['r']):

        if sequence[0] == 'r':
            self.osc = Oscillator(261.62)
        else:
            self.osc = Oscillator(sequence[0])

        self.output = Signal()
        self.sequence = sequence
        self.current_pos = 0

        self.bps = (float(bpm) / 60.0)
        self.update_frames = (1.0 / self.bps) * SAMPLE_RATE
        self.dt = 0

    def set_sequence(self, sequence):

        if sequence[0] == 'r':
            self.osc.set_freq(261.62)
        else:
            self.osc.set_freq(sequence[0])

        self.current_pos = 0
        self.dt = 0
        self.sequence = sequence

    def generate_frame(self):
        seq = self.sequence[self.current_pos % len(self.sequence)]

        self.dt += 1
        if self.dt > self.update_frames:
            self.current_pos += 1
            seq = self.sequence[self.current_pos % len(self.sequence)]
            self.dt = 0
            if seq != 'r':
                self.osc.set_freq(seq)

        self.osc.generate_frame()
        if seq == 'r':
            self.output.send(chr(127)) # rest, generate silence
        else:
            self.output.send(self.osc.output.poll())


class Sample:

    def __init__(self, path):
        w = wave.open(path, 'rb')
        self.data = bytearray(w.readframes(w.getnframes()))
        self.current_frame = 0

        self.output = Signal()

        if w.getsampwidth == 2:
            print "compressing sample to 8bit."
            new_data = bytearray()
            for i in range(0, len(self.data), 2):
                b = 256*ord(self.data[i-1]) + ord(self.data[i])
                b = int(b * (255.0/65535.0))
                new_data.append(b)
            self.data = new_data

        if w.getnchannels == 2:
            print "compressing sample to mono."
            new_data = bytearray()
            for i in range(0, len(self.data), 2):
                b = (int(self.data[i]) + int(self.data[i-1])) / 2
                new_data.append(b)
            self.data = new_data

        # TODO: Convert sample rate to desired

    def generate_frame(self):
        if self.current_frame > len(self.data):
            self.current_frame = 0
        self.current_frame += 1
        self.output.send(self.data[self.current_frame -1])


class RangeCompressor:

    def __init__(self, input, gain):
        self.input = input
        self.gain = gain # between 0.0 and 1.0, as its a compressor
        self.output = Signal()

    def set_gain(self, gain):
        self.gain = gain

    def generate_frame(self):
        b = self.input.poll()
        b = int((ord(b) - 127) * self.gain)
        b += 127
        self.output.send(chr(b))


class WaveInterface:

    def __init__(self, path):
        self.w = wave.open(path, 'wb')
        self.w.setnchannels(1)
        self.w.setsampwidth(1)
        self.w.setframerate(SAMPLE_RATE)

        self.entities = []

        self.final_output = None

    def generate_frames(self, n):
        buff = bytearray()
        for i in range(0, n):
            for e in self.entities:
                e.generate_frame()
            buff.append(self.final_output.poll())
        self.w.writeframes(buff)

    def generate_seconds(self, seconds):
        self.generate_frames(SAMPLE_RATE * seconds)

    def generate_beats(self, beats, bpm=80):
        n = int((1.0 / (float(bpm) / 60.0)) * SAMPLE_RATE) * beats
        self.generate_frames(n)

    def add_entity(self, entity):
        self.entities.append(entity)


if __name__ == "__main__":

    interface = WaveInterface("test.wav")

    seq_a = Sequencer(sequence = [130.81, 164.81, 196.00])
    interface.add_entity(seq_a)

    seq_b = Sequencer(sequence = [392.00, 329.63, 261.63])
    interface.add_entity(seq_b)

    combi = Mixer(seq_a.output, seq_b.output)
    interface.add_entity(combi)

    interface.final_output = combi.output

    interface.generate_beats(7)
