class Assigner(object):
    def __init__(self):
        data_file = open('raw/noveval.csv', 'r')
        self.transit_hash = {}
        for line in data_file:
            st_line = line.strip()
            alpha, number = st_line.split(',')
            self.transit_hash[alpha] = int(number)

    def letter_to_number(self, letter, octave):
        letter_val = self.transit_hash[letter]
        octave_val = {
            0: 0,
            1: 12,
            2: 24,
            3: 36,
            4: 48,
            5: 60,
            6: 72
        }
        return letter_val + octave_val[octave]

def grade_static_beat(key, chord, btas, vals):
    ret_hash = {
        'is_misspelled' : is_misspelled(chord, btas),
        'is_lt_doubled': is_lt_doubled
    }
    score = 1.0
    # Misspelled Chord              Unforgiveable   Static
    score -= 1.0
    # Double Leading Tone           Bad Bad  Static
    # Spacing                       Bad Bad Static
    
    # vii dim in 1st inv only       Bad     Static
    # Overlapping                   Eww      Static
    # Voice Crossing                Eww     Static
    # Double bass in 2nd inversion  Eww     Static
    # Double root of root position  Meh     Static
    pass

def grade_moving_chords(key, chord, prev_btas, prev_val, btas, val):
    score = 1.0
    # Parralel 5ths                 Awful   N - 1, N
    # Parralel 8vas                 Awful   N - 1, N
    score -= 0.5
    # Resolve LT -> Tonic (outer)   Bad Bad N - 1, N
    # *Resolve 7th of ch down step   Bad Bad  N - 1, N
    score -= 0.25
    # Melodic leap augmented        Eww      N-1, N
    # Consecutive 5th by contrary   Meh     N-1, N
    # Consecutive 8va by contrary   Meh     N-1, N
    # Hidden 5ths in outer voices   Meh     N-1, N
    score -= 0.25
    return score
