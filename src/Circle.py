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
OCTAVE  = 12

FLAT_CIRCLE = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
SHARP_CIRCLE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
CIRCLE = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']

C_FLAT_CIRCLE = ['C', 'Db', 'D', 'Eb', 'Fb', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'Cb']
G_FLAT_CIRCLE = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'Cb']
F_SHARP_CIRCLE = ['C', 'C#', 'D', 'D#', 'E', 'E#', 'F#', 'G', 'G#', 'A', 'A#', 'B']
#C_SHARP_CIRCLE = ['C', 'C#', 'D', 'D#', 'E', 'E#', 'F#', 'G', 'G#', 'A', 'A#', 'B#']
C_SHARP_CIRCLE = ['B#', 'C#', 'D', 'D#', 'E', 'E#', 'F#', 'G', 'G#', 'A', 'A#', 'B']

SHARP_DOMINATED = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
FLAT_DOMINATED = ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']


class Circle(object):
    
    def __init__(self, key, misc={}):
        """
        We may find it helpful to instantiate a tonic circle for us instead of using it statically.
        """
        self.tonic = key
        self.circle = SHARP_CIRCLE if (key in SHARP_DOMINATED or '#' in key) else FLAT_CIRCLE
        self.circle = CIRCLE if key == 'C' else self.circle
        parent_key = "String cheese"
        if 'parent' in misc.keys():
            parent_key = misc['parent']
        self.circle = FLAT_CIRCLE if parent_key in FLAT_DOMINATED else self.circle
        self.circle = C_FLAT_CIRCLE if parent_key == 'Cb' else self.circle
        self.circle = G_FLAT_CIRCLE if parent_key == 'Gb' else self.circle
        self.circle = F_SHARP_CIRCLE if parent_key == 'F#' else self.circle
        self.circle = C_SHARP_CIRCLE if parent_key == 'C#' else self.circle
        self.circle = C_SHARP_CIRCLE if key == 'G#' else self.circle
        self.tonic_val = self.circle.index(key)

    def generate_triad(self, quality='major', inversion=0, root_octave=3, bass=True):
        if quality == 'major':
            chord = self.__generate_major_triad()
        if quality == 'minor':
            chord = self.__generate_minor_triad()
        if quality == 'aug':
            chord = self.__generate_augmt_triad()
        if quality == 'dim':
            chord = self.__generate_dimin_triad()
        
#         chord = Rectifier.assign_octave(key=self.tonic, chord=chord, 
#                                         quality=quality, inversion=inversion, octave)
        return chord
        
    def generate_extended(self, quality='7', add={}, less={}, root_octave=3, bass=True):
        quality = str.lower(quality)
        if quality in ['dom7', '7']:
            chord = self.__generate_dom_7()
        if quality in ['maj7']:
            chord = self.__generate_maj_7()
        if quality in ['min7']:
            chord = self.__generate_min_7()
        if quality in ['halfdim7']:
            chord = self.__generate_halfdim7()
        if quality in ['dim7']:
            chord = self.__generate_dim7()
        return chord
    
    def __generate_dom_7(self):
        triad = self.generate_triad()
        seventh = self.circle[(self.tonic_val + MINOR_SEVENTH) % OCTAVE]
        triad.append(seventh)
        return triad
        
    def __generate_maj_7(self):
        triad = self.generate_triad()
        seventh = self.circle[(self.tonic_val + MAJOR_SEVENTH) % OCTAVE]
        triad.append(seventh)
        return triad
    
    def __generate_min_7(self):
        triad = self.generate_triad(quality='minor')
        seventh = self.circle[(self.tonic_val + MINOR_SEVENTH) % OCTAVE]
        triad.append(seventh)
        return triad
    
    def __generate_halfdim7(self):
        triad = self.generate_triad(quality='dim')
        seventh = self.circle[(self.tonic_val + MINOR_SEVENTH) % OCTAVE]   
        triad.append(seventh)
        return triad
    
    def __generate_dim7(self):
        triad = self.generate_triad(quality='dim')
        seventh = self.circle[(self.tonic_val + DIMINISHED_SEVENTH) % OCTAVE]
        triad.append(seventh)
        return triad
        
    def __generate_augmt_triad(self):
        third = self.circle[(self.tonic_val + MAJOR_THIRD) % OCTAVE]
        fifth = self.circle[(self.tonic_val + AUGMENTED_FIFTH) % OCTAVE]
        return [self.tonic, third, fifth]
    
    def __generate_major_triad(self):
        third = self.circle[(self.tonic_val + MAJOR_THIRD) % OCTAVE]
        fifth = self.circle[(self.tonic_val + PERFECT_FIFTH) % OCTAVE]
        return [self.tonic, third, fifth]
    
    def __generate_minor_triad(self):
        third = self.circle[(self.tonic_val + MINOR_THIRD) % OCTAVE]
        fifth = self.circle[(self.tonic_val + PERFECT_FIFTH) % OCTAVE]
        return [self.tonic, third, fifth]
    
    def __generate_dimin_triad(self):
        third = self.circle[(self.tonic_val + MINOR_THIRD) % OCTAVE]
        fifth = self.circle[(self.tonic_val + DAT_TRITONE) % OCTAVE]
        return [self.tonic, third, fifth]        