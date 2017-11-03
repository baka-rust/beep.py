import sys
sys.dont_write_bytecode = True

import pyaudio

from beep.elements.oscillator import Oscillator
from beep.elements.compressor import Compressor
from beep.constants import SAMPLE_RATE

o = Oscillator()
rack_head = Compressor(o, .1)


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paUInt8,
                channels=1,
                rate=SAMPLE_RATE,
                output=True)

for i in range(0, 50):
    stream.write(rack_head.gen_frame())

stream.stop_stream()
stream.close()
p.terminate()
