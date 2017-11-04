import sys
sys.dont_write_bytecode = True

import pyaudio

from beep.elements.oscillator import Oscillator
from beep.elements.compressor import Compressor
from beep.elements.sequencer import Sequencer
from beep.constants import SAMPLE_RATE, FRAME_SIZE

s = Sequencer([261.63, 329.63, 392.00, 493.88])

def frames_for_seconds(s):
    return int((SAMPLE_RATE * s) / FRAME_SIZE)


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paUInt8,
                channels=1,
                rate=SAMPLE_RATE,
                output=True)


for i in range(0, frames_for_seconds(1)):
    stream.write(s.gen_frame())


stream.stop_stream()
stream.close()
p.terminate()
