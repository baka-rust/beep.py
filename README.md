# beep.py
A lil' python lib for making 8bit music. Here's a list of all current available entities (aka simulated audio elements).

### Signal
A simple class that allows you to pass data (singular bytes usually, because of the 8-bit LPCM format that beep.py asssumes) between entities.

### Oscillator
A wave-table oscillator. Capable of generating its own tables like sine, saw, and square.

### Mixer
Simple soft-clipping mixer that combines multiple signals. It simply takes a weighted sum of input elements.

### Sequencer
A Sequencer. Contains a singular oscillator and steps through defined note frequencies at a constant pace (a beat). When it's through with a sequence, it wraps around. It also can have rests, defined as `r` in the sequence (otherwise a list of floats).

### Sample
A sample, aka a chunk of audio data. Assumed to be a .wav file. It will automatically convert the sample to 8-bit mono on creation, but currently assumes a sample rate of 44100 (as defined in beep.py, thus it's potentially variable). Not really usable until I write a "Sampler" aka something in charge of sequencing and playing samples.
Still, you can treat it like any other element with an output, and it'll just loop through the sample.

### RangeCompressor
A simple compressor that takes a gain (between 0 and 1) and applies it to a signal.

### WaveInterface
The big dude who does all of the heavy lifting. It handles the output .wav file headers and creation.

When adding a new element to your song, make sure to call `add_entity` on your WaveInterface. That way, frames will get generated correctly.



# song.py
An interface for creating lil tunes using beep.py.
It allows you to define your entity rack in a yaml file, and your sequences in a csv file.
Pretty handy!

### Example rack.yaml
This makes a compressor with a gain of .35 at the root with a mixer for input, which in turn mixes three sequencers called "high", "mid", and "bass". Depending on the entity, you can have a "signals" field, or a singular "signal".
You can sorta nest a ton of these using beep.py elements. Pretty nifty

```yaml
rack:
    type: "RangeCompressor"
    gain: 0.35
    signal:
        type: "Mixer"
        signals:
            - name: "high"
              type: "Sequencer"
              waveform: "square"
            - name: "mid"
              type: "Sequencer"
              waveform: "sine"
            - name: "bass"
              type: "Sequencer"
              waveform: "square"

```

### Example sequences.csv
Sequences are held in a csv file, with the columns being titled after the named sequence they're assigned to. These names are related to the `name` field in the yaml file.
Notes must be in this format: "{name}{s}{level}", where s is optional and stands for sharp. Ex: "c4" is middle c, whereas "cs5" is the c-sharp an octave above middle c.

```csv
high,mid,bass
g4,e4,c2
g4,e4,e2
g4,e4,c2
g4,e4,e2
r,r,r
b4,g4,e2
b4,g4,e2
g4,e4,c2
g4,e4,c2
r,r,r
b4,g4,e2
b4,g4,e2
g4,e4,c2
g4,e4,c2
```
