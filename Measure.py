from copy import deepcopy

class Measure(object):
    def __init__(self, parent_time):
        self.n_beats = parent_time.top
        self.beats_remaining = parent_time.top
        self.chord_assign_index = 0

        self.beat_chords = {}
        for i in range(self.n_beats):
            self.beat_chords[i] = 3

        self.filled = True if self.beats_remaining == 0 else False

    def fill(self, chord, n_beats):
        # I could pass in the parent_time too, but then im worried someone like me would
        # be tempted to restart beats_remaining, but fill is called after instantiation

        self.beat_chords[self.chord_assign_index] = deepcopy(chord)
        self.chord_assign_index += 1

        self.beats_remaining -= 1
        # print(self.beat_chords)
        self.filled = True if self.beats_remaining == 0 else False
        
    def get_chord_locations(self):
        return self.beat_chords

    def __str__(self):
        retstr = "["
        for i in range(self.n_beats):
            chord = self.beat_chords[i]
            # print(chord)
            retstr += "%2s%5s" % (self.beat_chords[i].root, self.beat_chords[i].quality)
        retstr += "]\n"
        return retstr