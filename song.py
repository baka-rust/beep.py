# A higher level interface for beep.py, lets you make tunes and stuff
# you can use a yaml config to define your entity rack,
# and a csv file to define your sequences

import beep
import csv
import math
import re
import yaml


class Song:

    def __init__(self, output_path, bpm):
        self.interface = beep.WaveInterface(output_path)

        self.bpm = bpm
        self.named_elements = {}
        self.max_sequence_length = 0

        self.interface.final_output = None

        self.note_match = re.compile('(\D{1,2})(\d+)')
        self.const_a = 1.059463094359
        self.scale = {
            "a": 0, "as": 1, "b": 2, "c": 3, "cs": 4, "d": 5,
            "ds": 6, "e": 7, "f": 8, "fs": 9, "g": 10, "gs": 11
        }

    def load_entities(self, elements_yaml_path):
        f = open(elements_yaml_path)
        elements_yaml = f.read()
        e = yaml.load(elements_yaml)

        self.rack_root = self.create_entity_recursive(e["rack"])
        self.interface.final_output = self.rack_root.output

    def create_entity_recursive(self, entity_dict):
        entity_type = entity_dict.get("type")

        if entity_type == "Mixer":
            e = beep.Mixer()
            for child in entity_dict.get("signals", []):
                child_e = self.create_entity_recursive(child)
                e.add_signal(child_e.output)
        elif entity_type == "Sequencer":
            e = beep.Sequencer(bpm = entity_dict.get("bpm", self.bpm))
            if "waveform" in entity_dict:
                waveform = entity_dict.get("waveform")
                if waveform == "sine":
                    e.osc.set_wavetable_sin()
                elif waveform == "saw":
                    e.osc.set_wavetable_saw()
                elif waveform == "square":
                    e.osc.set_wavetable_square()
        elif entity_type == "RangeCompressor":
            e = beep.RangeCompressor(None, entity_dict.get("gain", 1.0))
            if "signal" in entity_dict:
                child_e = self.create_entity_recursive(entity_dict.get("signal"))
                e.input = child_e.output

        if "name" in entity_dict:
            self.named_elements[entity_dict.get("name")] = e
        self.interface.add_entity(e)
        return e

    def load_sequences_csv(self, sequences_csv_path):
        sequences = {}

        csv_file = open(sequences_csv_path)
        dump = csv.DictReader(csv_file, delimiter=',')
        for row in dump:
            for elt in row:
                if not elt.replace(' ', '') in sequences:
                    sequences[elt.replace(' ', '')] = []
                sequences[elt.replace(' ', '')].append(row[elt].replace(' ', ''))

        for sequencer_name in sequences:
            self.decode_sequence_simple(sequencer_name, sequences[sequencer_name])


    def decode_sequence_simple(self, sequencer_name, sequence):
        freq_sequence = []
        for note in sequence:
            if note == 'r':
                freq_sequence.append('r')
            else:
                freq_sequence.append(self.calculate_note_freq(note))
        self.add_sequence(sequencer_name, freq_sequence)

    def calculate_note_freq(self, note):
        note_parsed = self.note_match.findall(note)[0]
        note_key = note_parsed[0]
        note_offset = int(note_parsed[1]) - 4
        steps_away = self.scale[note_key] + (12 * note_offset)
        freq = 440.0 * math.pow(self.const_a, steps_away)
        return freq

    def add_sequence(self, sequencer_name, sequence):
        if len(sequence) > self.max_sequence_length:
            self.max_sequence_length = len(sequence)
        if sequencer_name in self.named_elements:
            self.named_elements[sequencer_name].set_sequence(sequence)

    def generate(self):
        self.interface.generate_beats(self.max_sequence_length, bpm=self.bpm)

s = Song("test.wav", 120)

s.load_entities("example/rack.yaml")
s.load_sequences_csv("example/sequences.csv")

s.generate()
