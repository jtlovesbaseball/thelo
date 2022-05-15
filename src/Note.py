OCTAVE_ORDER = ['Cb', 'C', 'Db', 'C#', 'D', 'D#', 'Eb', 'E', 'Fb', 'E#', 'F', 'F#', 'Gb', 'G',
                'Ab', 'G#', 'A', 'A#', 'Bb', 'B', 'B#']
NOTEVALS_SIMPLE = {1: 'Quarter', 2: 'Half', 3: 'Dotted Half', 4: 'Whole'}
SIMPLE_ORDER = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

from functools import total_ordering


class DrawableNote(object):
    def __init__(self, note, start_beat, num_beats, beat_value, measure):
        self.letter = note.letter
        self.octave = note.octave
        self.lookup = note.lookup
        self.bass = note.is_bass
        self.flipped = note.is_flipped
        self.start_beat = start_beat
        self.num_beats = num_beats
        self.beat_value = beat_value
        self.measure = measure
        self.order = note.order
        self.absolute_order = note.absolute_order
        self.pure_order = note.pure_order
        self.gradeval = -1
        # Add logic to decrement order and abs order of E#
        
    def in_measure(self, m):
        return True if m == self.measure else False
        
    def increment_beat(self):
        self.num_beats += 1

    @staticmethod
    def create(letter, octave, bass, flip, start_beat,
               num_beat, beat_val, measure):
        n = Note(letter, octave, is_bass=bass, is_flipped=flip)
        dn= DrawableNote(n, start_beat, num_beat, beat_val, measure)
        return dn
        
    def __str__(self):
        return "%s Note %s (beat %d)" % (NOTEVALS_SIMPLE[self.num_beats], self.lookup, self.start_beat + 1)


@total_ordering
class Note(object):
    def __init__(self, letter, octave, is_bass=False, is_flipped=False, ao_modifier=0):
        self.letter = letter
        self.octave = octave
        self.is_bass = is_bass
        self.is_flipped = is_flipped
        self.lookup = "%s%d" % (letter, octave)
        self.selected = False
        self.unselected = False
        self.order = SIMPLE_ORDER.index(self.letter[0])
        self.absolute_order = ((self.octave - 2) * 8) + self.order
        self.pure_order = self.absolute_order
        self.absolute_order += ao_modifier


    def select(self):
        self.selected = True
        self.unselected = False
    
    def unselect(self):
        self.unselected = True
        self.selected = False

    def return_up_octave(self):
        new = Note(self.letter, self.octave + 1, is_bass=self.is_bass, is_flipped=self.is_flipped)
        return new
    
    def __str__(self):
        if self.unselected:
            return "Unselected %s" % self.lookup
        if self.selected:
            return self.lookup
        return "Unselected %s" % self.lookup
    
    def __lt__(self, o):
        if self.octave < o.octave:
            return True
        if self.octave > o.octave:
            return False
        
        self_index = OCTAVE_ORDER.index(self.letter)
        othe_index = OCTAVE_ORDER.index(o.letter)
        
        return self_index < othe_index
    
    def __eq__(self, o):
        if self.lookup == o.lookup:
            if self.octave == o.octave:
                return True
        return False