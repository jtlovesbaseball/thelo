from Circle import Circle as c
from Chord import Chord as ch

MINOR_SECOND = 1
MAJOR_SECOND = 2
MINOR_THIRD = 3
MAJOR_THIRD = 4
PERFECT_FOURTH = 5
DAT_TRITONE = 6
PERFECT_FIFTH = 7
AUGMENTED_FIFTH = 8
MINOR_SIXTH = 8
MAJOR_SIXTH = 9
DIMINISHED_SEVENTH = 9
MINOR_SEVENTH = 10
MAJOR_SEVENTH = 11
OCTAVE        = 12

FLAT_CIRCLE = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
SHARP_CIRCLE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
CIRCLE = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']

SHARP_DOMINATED = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
FLAT_DOMINATED = ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']

MAJOR_MODE = [0, 2, 4, 5, 7, 9, 11, 12]
MINOR_MODE = [0, 2, 3, 5, 7, 8, 10, 12]

class Key(object):
    
    def __init__(self, key, tonality='major', misc={}):
        """
        We may find it helpful to instantiate a tonic circle for us instead of using it statically.
        """
        self.key = None
        if len(key) == 2 and key[-1] == 'b':
            self.key = str(key[0]).upper() + 'b'
        else:
            self.key = str(key).upper()
        self.tonality = tonality
        
        #I wanted this line to have a ternary operator but thats why I have to make the seperate Am CM keys below
        self.circle = SHARP_CIRCLE if (self.key in SHARP_DOMINATED or '#' in self.key) else FLAT_CIRCLE
        self.circle = CIRCLE if self.key == 'C' else self.circle
        self.tonic_val = self.circle.index(self.key)
        self.indicies = [(self.tonic_val + i) % OCTAVE for i in MAJOR_MODE]
        self.notes = [self.circle[i] for i in self.indicies]
        
        if str(key).lower() == 'a' and tonality == 'minor':
            self.notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        if str(key).lower() == 'c' and tonality == 'major':
            self.notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        
        if tonality == 'major':
            self.tonic =  c(self.notes[0]).generate_triad('major')
            self.supertonic =  c(self.notes[1]).generate_triad('minor')
            self.mediant = c(self.notes[2]).generate_triad('minor')
            self.subdominant = c(self.notes[3]).generate_triad('major')
            self.dominant = c(self.notes[4]).generate_triad('major')
            self.submediant = c(self.notes[5]).generate_triad('minor')
            self.leadingtone = c(self.notes[6]).generate_triad('dim')
            self.subtonic = None # I dont really understand music theory?
        else:
            self.tonic =  c(self.notes[0]).generate_triad('minor')
            self.supertonic =  c(self.notes[1]).generate_triad('dim')
            self.mediant = c(self.notes[2]).generate_triad('major')
            self.subdominant = c(self.notes[3]).generate_triad('minor')
            self.dominant = c(self.notes[4]).generate_triad('minor')
            self.submediant = c(self.notes[5]).generate_triad('major')
            self.leadingtone = c(self.notes[6]).generate_triad('dim')
            self.subtonic = c(self.notes[6]).generate_triad('major')
            
    def get_key(self):
        return {'pitch': self.key, 'tonality': self.tonality}
    
    def get_chord(self, degree, dim_minor_7=True):
        degree = int(degree)
        ext = True if int(degree) > 8 else False
        roman = (degree - 1) % 8
        quality_tonality = {
        0: {'major': 'major', 'minor': 'minor'},
        1: {'major': 'minor', 'minor': 'dim'},
        2: {'major': 'minor', 'minor': 'major'},
        3: {'major': 'major', 'minor': 'minor'},
        4: {'major': 'major', 'minor': 'minor'},
        5: {'major': 'minor', 'minor': 'major'},
        6: {'major': 'dim', 'minor': 'dim'}
        }
        roman_quality= quality_tonality[roman][self.tonality]
        if roman == 6 and self.tonality == 'minor' and not dim_minor_7:
            roman_quality = 'major'
        chord = c(self.notes[roman]).generate_triad(roman_quality)
        chord_obj = ch(chord, self.notes[roman], roman_quality) # Comment if dud
        return {'degree': degree, 'key': self.notes[roman], 'quality': roman_quality, 'chord': chord_obj}
    
    def simple_str(self):
        return "%s %s" % (self.key, self.tonality)
            
    def __str__(self):
        retstr = "%s %s: " % (self.key, self.tonality)
        for note in self.notes:
            retstr += "%-3s" % note
        retstr += "\n\n"
        retstr += """
        Tonality: %s
        Tonic: %s
        Supertonic: %s
        Mediant: %s
        Subdominant: %s
        Dominant: %s
        Submediant: %s
        Leading Tone: %s
        Subtonic: %s
        """ % (self.tonality, self.tonic, self.supertonic, self.mediant, self.subdominant, self.dominant,
              self.submediant, self.leadingtone, "N/A" if self.tonality == 'major' else self.subtonic)
        retstr += "\n\n"
        return retstr