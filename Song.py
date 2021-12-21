from util import MajorChordTransition
from Measure import Measure

class Song(object):
    def __init__(self, name, composer, signature):
        self.name = name
        self.composer = composer
        self.signature = signature
        self.chords = []
        self.measures = []
        self.tonal_status = "1" # Chord we're currently on
        self.major_ct = MajorChordTransition()
        
    def change_time(self, time):
        self.signature.time = time
        
    def change_key(self, key):
        self.signature.key = key
        
    def fill_measures(self, chord):
        beats_remaining = chord.n * self.signature.time.top
        self.measures.append(Measure(self.signature.time))
        #print(len(self.measures))
        while beats_remaining > 0:
            if not self.measures[-1].filled:
                self.measures[-1].fill(chord, n_beats=min(self.signature.time.top, beats_remaining))
            else:
                self.measures.append(Measure(self.signature.time))
                self.measures[-1].fill(chord, n_beats=min(self.signature.time.top, beats_remaining))
            beats_remaining -= 1
      
    def generate_chords(self, n):
        for i in range(n):
            self.generate_next_chord()
        
        for c in self.chords:
            self.fill_measures(c)
            
    def generate_next_chord(self):
        generated_chord = self.signature.key.get_chord(degree=self.tonal_status)     
        self.chords.append(generated_chord['chord'])
        self.tonal_status = self.major_ct.transition(self.tonal_status)
        
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
        
        