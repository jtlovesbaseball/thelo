from util import MajorChordTransition

class Song(object):
    def __init__(self, name, composer, signature):
        self.name = name
        self.composer = composer
        self.signature = signature
        self.chords = []
        self.tonal_status = "1" # Chord we're currently on
        self.major_ct = MajorChordTransition()
        
    def change_time(self, time):
        self.signature.time = time
        
    def change_key(self, key):
        self.signature.key = key
        
    def generate_chords(self, n):
        for i in range(n):
            self.generate_next_chord()
        
    def generate_next_chord(self):
        generated_chord = self.signature.key.get_degree_chord(self.tonal_status)
        self.chords.append(generated_chord)
        self.tonal_status = self.major_ct.transition(self.tonal_status)
        
    def __str__(self):
        chord_str = """"""
        for chord in self.chords:
            chord_str += "\n%s\n" % chord
        retstr = """Song Title: "%s"
Composer: %s
Signature info: %s
Chords: %s""" % (self.name, self.composer, self.signature.__str__(),chord_str)
        return retstr
        
        