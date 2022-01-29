from Voice import Voice
from Piece import Piece

class Composer(object):
    def __init__(self, song=None):
        self.song = song
        self.voices = {}
        
    def learn(self, song):
        self.song = song

    def compose_fourvoice(self, song=None):
        self.generate_fourvoice(song)
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
                valid_notes = list(filter(lambda x: x.letter == note , self.voices[voice].notes[beat_idx]))
                for beat in self.voices[voice].notes[beat_idx]:
                    if beat == valid_notes[0]:
                        beat.selected = True
                    else:
                        beat.unselected = True
    
    def __str__(self):
        voicestr = ""
        for v in self.voices:
            voicestr += self.voices[v].__str__()
            voicestr += "\n"
        retstr = """Song: %s
Voices:
%s""" % (self.song, voicestr)
        return retstr
