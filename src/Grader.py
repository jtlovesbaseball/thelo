from gradeutils import Assigner
import gradeutils as gutil

class Grader(object):
    def __init__(self, piece=None, mode='default'):
        self.mode = mode
        self.piece = piece
        self.assigner = Assigner()

    def learn(self, piece):
        self.piece = piece

    def switch_mode(self, mode):
        self.mode = mode

    def grade(self):
        if self.mode == 'default':
            self.grade_default()

    def grade_default(self):
        voices = self.piece.voices
        tracks = self.piece.tracks
        chords = self.piece.song.chords
        key = self.piece.song.signature.key.key
        prev_orders = {}
        for v in voices:
            prev_orders[v] = -1
        prev_BTAS = [prev_orders['B'], prev_orders['T'],
                     prev_orders['A'], prev_orders['S']]
        prev_vals = [-1, -1, -1, -1]
        static_scores = []
        moving_scores = []
        for i, chord in enumerate(chords):
            song_key = self.piece.song.signature.key.key
            chord_key = chord.root
            this_BTAS = [tracks['B'][i], tracks['T'][i],
                         tracks['A'][i], tracks['S'][i]]
            if i > 0 :
                prev_vals = [self.assigner.letter_to_number(x.letter, x.octave) for x in prev_BTAS]
            this_vals = [self.assigner.letter_to_number(x.letter, x.octave) for x in this_BTAS]

            print("Wakka")
            prev_BTAS = this_BTAS
            prev_vals = this_vals

            static_val = gutil.grade_static_beat(chord, this_BTAS, this_vals)
            static_scores.append(static_val)
            if i > 0:
                moving_val = gutil.grade_moving_chords(chord, prev_BTAS, prev_vals,
                                                       this_BTAS, this_vals)
                moving_scores.append(moving_val)

            #Sins
            # Misspelled Chord              Unforgiveable   Static
            # Parralel 5ths                 Awful   N - 1, N
            # Parralel 8vas                 Awful   N - 1, N
            # Double Leading Tone           Bad Bad  Static
            # Resolve LT -> Tonic (outer)   Bad Bad N - 1, N
            # Spacing                       Bad Bad Static
            #*Resolve 7th of ch down step   Bad Bad  N - 1, N
            # vii dim in 1st inv only       Bad     Static
            # Overlapping                   Eww      Static
            # Voice Crossing                Eww     Static
            # Melodic leap augmented        Eww      N-1, N
            # Double bass in 2nd inversion  Eww     Static
            # Double root of root position  Meh     Static
            # Consecutive 5th by contrary   Meh     N-1, N
            # Consecutive 8va by contrary   Meh     N-1, N
            # Hidden 5ths in outer voices   Meh     N-1, N


if __name__ == '__main__':
    pass
