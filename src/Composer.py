import random
from Voice import Voice
from Piece import Piece
from Note import Note

class Composer(object):
    def __init__(self, song=None):
        self.song = song
        self.voices = {}
        
    def learn(self, song):
        self.song = song

    def compose_fourvoice(self, method='naive', song=None):
        self.generate_fourvoice(song)
        if method == 'naive':
            self.select_fourvoice_naive()
        if method == 'random':
            self.select_fourvoice_random()
        if method == 'root':
            self.select_fourvoice_root()
        finished = self.finish_piece(song)
        return finished
        
    def finish_piece(self, song):
        song = song if song is not None else self.song
        finished_piece = Piece(song, self.voices)
        return finished_piece
                
    def generate_fourvoice(self, song):
        song = song if song is not None else self.song
        reg_beat_measures = song.signature.time.top
        beats_req = len(song.song_beats)
        for voice in ["S", "A", "T", "B"]: # Sopranno, Alto, Tenor, Bass
            self.voices[voice] = Voice(voice, reg_beat_measures, beats_req)
        for beat in range(beats_req):
            beat_chord = self.song.get_chord(beat)
            for voice in ["S", "A", "T", "B"]: # Sopranno, Alto, Tenor, Bass
                self.voices[voice].generate_possible_fourvoice(beat_chord, beat)

    @staticmethod
    def bound_list(notelist, lower, upper):
        outlist = []
        for note in notelist:
            if lower <= note <= upper:
                outlist.append(note)
        return outlist

    def select_fourvoice_naive(self):
        for beat_idx in range(len(self.song.song_beats.keys())):
            chord = self.song.song_beats[beat_idx]
            for voice in ["S", "A", "T", "B"]:
                note = None
                if voice == "S":
                    note = chord.notes[2]
                if voice == "T":
                    note = chord.notes[0]
                if voice == "A":
                    note = chord.notes[1]
                if voice == "B":
                    note = chord.notes[0]
                valid_notes = list(filter(lambda x: x.letter == note , self.voices[voice].notes[beat_idx]))
                for beat in self.voices[voice].notes[beat_idx]:
                    if beat == valid_notes[0]:
                        beat.selected = True
                    else:
                        beat.unselected = True

    def select_fourvoice_random(self):
        for beat_idx in range(len(self.song.song_beats.keys())):
            chord = self.song.song_beats[beat_idx]
            random.randint(0, 2)
            for voice in ["S", "A", "T", "B"]:
                note = None
                if voice == "S":
                    note = chord.notes[random.randint(0, 2)]
                if voice == "T":
                    note = chord.notes[random.randint(0, 2)]
                if voice == "A":
                    note = chord.notes[random.randint(0, 2)]
                if voice == "B":
                    note = chord.notes[random.randint(0, 2)]
                valid_notes = list(filter(lambda x: x.letter == note , self.voices[voice].notes[beat_idx]))
                random.shuffle(valid_notes)
                for beat in self.voices[voice].notes[beat_idx]:
                    if beat == valid_notes[0]:
                        beat.selected = True
                    else:
                        beat.unselected = True

    def select_fourvoice_root(self):
        for beat_idx in range(len(self.song.song_beats.keys())):
            chord = self.song.song_beats[beat_idx]
            for voice in ["S", "A", "T", "B"]:
                note = None

                if voice == "S":
                    note = chord.notes[2]
                if voice == "T":
                    note = chord.notes[0]
                if voice == "A":
                    note = chord.notes[1]
                if voice == "B":
                    note = chord.notes[0]

                valid_notes = list(filter(lambda x: x.letter == note, self.voices[voice].notes[beat_idx]))
                #  This isn't going to work. I made the fault assumption that if
                #  the alto was singing the 3rd and the soprano was singing the
                #  5th that these bounds would ensure root position. Doesn't
                #  work for minor 3rds
                if voice == "S":
                    below = Note(letter='C#', octave=4) # Do this smarter to STAB!
                    above = Note(letter='Db', octave=5)
                    valid_notes = Composer.bound_list(valid_notes, below, above)
                if voice == "T":
                    below = Note(letter='G', octave=3) # Do this smarter to STAB!
                    above = Note(letter='Gb', octave=4)
                    valid_notes = Composer.bound_list(valid_notes, below, above)
                if voice == "A":
                    below = Note(letter='B', octave=3) # Do this smarter to STAB!
                    above = Note(letter='Bb', octave=4)
                    valid_notes = Composer.bound_list(valid_notes, below, above)
                if voice == "B":
                    below = Note(letter='G', octave=2) # Do this smarter to STAB!
                    above = Note(letter='Gb', octave=3)
                    valid_notes = Composer.bound_list(valid_notes, below, above)
                for beat in self.voices[voice].notes[beat_idx]:
                    if voice == 'T':
                        beat.is_bass = False
                    try:
                        if beat == valid_notes[0]:
                            beat.selected = True
                        else:
                            beat.unselected = True
                    except IndexError:
                        pass
    
    def __str__(self):
        voicestr = ""
        for v in self.voices:
            voicestr += self.voices[v].__str__()
            voicestr += "\n"
        retstr = """Song: %s
Voices:
%s""" % (self.song, voicestr)
        return retstr
