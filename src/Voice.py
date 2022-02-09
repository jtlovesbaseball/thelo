from Note import Note
import util
import json

FOUR_VOICE = {
    'B': {'E': (2, 3, 4), 'Fb': (2, 3, 4), 'F': (2, 3), 'E#': (2, 3), 'F#': (2, 3), 'Gb': (2, 3), 'G': (2, 3), 'Ab': (2, 3), 'G#': (2, 3),
          'A': (2, 3), 'A#': (2, 3), 'Bb': (2, 3), 'Cb': (3, 4), 'B': (2, 3),  'B#': (2, 3), 'C': (3, 4), 'C#': (3, 4), 'Db': (3, 4), 'D': (3, 4),
          'Eb': (3, 4), 'D#': (3, 4)},
    'T': {'C': (3, 4, 5), 'B#': (3, 4), 'C#': (3, 4), 'Db': (3, 4), 'D': (3, 4), 'Eb': (3, 4), 'D#': (3, 4), 'E': (3, 4), 'Fb': (3, 4),
          'F': (3, 4), 'E#': (3, 4), 'F#': (3, 4), 'Gb': (3, 4), 'G': (3, 4), 'Ab': (3, 4), 'G#': (3, 4), 'A': (3, 4),
          'Bb': (3, 4), 'A#': (3, 4), 'B': (3, 4), 'Cb': (3, 4)},
    'A': {'F': (3, 4, 5), 'E#': (3, 4, 5), 'F#': (3, 4), 'Gb': (3, 4), 'G': (3, 4), 'Ab': (3, 4), 'G#': (3, 4), 'A': (3, 4), 'Bb': (3, 4),
          'A#': (3, 4), 'B': (3, 4), 'Cb': (4, 5), 'B#': (3, 4), 'C': (4, 5), 'C#': (4, 5), 'Db': (4, 5), 'D': (4, 5), 'Eb': (4, 5),
          'D#': (4, 5), 'E': (4, 5), 'Fb': (4, 5)},
    'S': {'C': (4, 5, 6), 'B#': (4, 5), 'C#': (4, 5), 'Db': (4, 5), 'D': (4, 5), 'Eb': (4, 5), 'D#': (4, 5), 'E': (4, 5), 'Fb': (4, 5), 'F': (4, 5), 'E#': (4, 5),
          'F#': (4, 5), 'Gb': (4, 5), 'G': (4, 5), 'Ab': (4, 5), 'G#': (4, 5), 'A': (4, 5), 'Bb': (4, 5), 
          'A#': (4, 5), 'B': (4, 5), 'Cb': (5, 6)}
}

NAMED = {'B': 'Bass', 'R': 'Baritone', 'T': 'Tenor', 'A': 'Alto', 'Z': 'Mezzo-Soprano', 'S': 'Soprano'}

class Voice(object):
    def __init__(self, voice, beat_measures, beats_to_fill):
        self.voice = voice
        self.named = NAMED[voice] if voice in set(NAMED.keys()) else "Custom Voice"
        self.beats_per_measure = beat_measures
        self.total_beats = beats_to_fill
        self.notes = {}
        
    def generate_possible_fourvoice(self, chord, beat):
        relevant_hash = FOUR_VOICE[self.voice]
        chord_notes = chord.notes
        for cn in chord_notes:
            octaves = relevant_hash[cn]
            for o in octaves:
                if beat not in self.notes:
                    self.notes[beat] = []
                b = Note(cn, o, is_bass=True if self.voice in ['B', 'T'] else False, is_flipped=True if self.voice in ['T', 'S'] else False)
                self.notes[beat].append(b)
        self.notes[beat].sort()
        
    def __str__(self):
        retstr = "%s Voice Note assignments: %s" % (self.named, json.dumps(self.notes, cls=util.NoteEncoder, 
                                                                           sort_keys=False, indent=1))
        return retstr