from util import MajorChordTransition
from Measure import Measure
import json
import jsonpickle

class Song(object):
    def __init__(self, name, composer, signature, original=None):
        self.name = name
        self.composer = composer
        self.signature = signature
        self.original = original
        self.chords = []
        self.measures = []
        self.tonal_status = "1" # Chord we're currently on
        self.major_ct = MajorChordTransition()
        self.beat_index = 0
        self.song_beats = {}
        
    def change_time(self, time):
        self.signature.time = time
        
    def change_key(self, key):
        self.signature.key = key
        
    def fill_measures(self, chord, fourvoice=False):
        beats_remaining = chord.n * self.signature.time.top
        
        if len(self.measures) == 0 or self.measures[-1].filled:
            self.measures.append(Measure(self.signature.time))
        
        beats_remaining = 1 if beats_remaining < 0 else beats_remaining  # Fourvoice hack for one beat
            
        while beats_remaining > 0:
            self.song_beats[self.beat_index] = chord
            self.beat_index += 1
            if not self.measures[-1].filled:
                self.measures[-1].fill(chord, n_beats=min(self.signature.time.top, beats_remaining))
            else:
                self.measures.append(Measure(self.signature.time))
                self.measures[-1].fill(chord, n_beats=min(self.signature.time.top, beats_remaining))
            beats_remaining -= 1
      
    def generate_chords(self, n, fourvoice=True):
        for i in range(n):
            self.generate_next_chord(fourvoice)
        
        for c in self.chords:
            self.fill_measures(c)
            
    def generate_next_chord(self, fourvoice, n=1):
        n = -1 if fourvoice else n
        generated_chord = self.signature.key.get_chord(degree=self.tonal_status, n=n)     
        self.chords.append(generated_chord['chord'])
        self.tonal_status = self.major_ct.transition(self.tonal_status)
        
    def get_chord(self, beat):
        str_keys = True if type(list(self.song_beats.keys())[0]) == str else False
        beat = str(beat) if str_keys else beat
        return self.song_beats[beat]

    def serialize(self, filename):
        obj = jsonpickle.encode(self)
        with open(filename, 'w') as ost:
            json.dump(obj, ost)

    @staticmethod
    def deserialize(filename):
        j = jsonpickle.decode(json.load(open(filename, 'r')))
        return j

    def __str__(self):
        chord_str = """"""
        measure_str = """"""
        for chord in self.chords:
            chord_str += "\n%s\n" % chord.__str__()
        for measure in self.measures:
            measure_str += '%s' % measure.__str__()
        retstr = """Song Title: "%s"
Composer: %s
Signature info: %s
Chords: %s
Measures: 
%s""" % (self.name, self.composer, self.signature.__str__(), chord_str, measure_str)
        return retstr
        
        