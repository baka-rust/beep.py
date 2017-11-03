# beep.py

A lil' python lib for making 8bit music. Here's a list of the current available elements (aka simulated audio components).

## Implemented

### Oscillator
A wave-table oscillator. Will be capable of generating its own tables like sine, saw, and square.

### Compressor

A simple compressor that takes a gain (between 0 and 1) and applies it to a signal

## Coming Up

### Mixer
Simple soft-clipping mixer that combines multiple signals. It simply takes a weighted sum of input elements.

### Sequencer

A Sequencer. Contains a singular oscillator and steps through defined note frequencies at a constant pace (a beat). When it's through with a sequence, it wraps around. It also can have rests, defined as r in the sequence (otherwise a list of floats).

### Sample

A sample, aka a chunk of audio data. Assumed to be a .wav file. It will automatically convert the sample to 8-bit mono on creation, but currently assumes a sample rate of 44100 (as defined in constants.py, thus it's potentially variable). Not really usable until I write a "Sampler" aka something in charge of sequencing and playing samples. Still, you can treat it like any other element with an output, and it'll just loop through the sample.
