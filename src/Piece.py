from Note import Note
from Note import DrawableNote
import util2 as utilcv2
import cv2
from fpdf import FPDF
import json
import jsonpickle

MEASURES_PER_PAGE = 16


class Piece(object):
    def __init__(self, song, voices):
        self.song = song
        self.voices = voices
        self.tracks = {}
        self.beats_per_measure = self.song.signature.time.top # Change back to bottom if it fucks
        self.measures = (len(self.voices['B'].notes.keys()) / self.beats_per_measure) + \
                        (1 if len(self.voices['B'].notes.keys()) % self.beats_per_measure != 0 else 0)
        for v in self.voices:
            self.tracks[v] = []
        self.write()
        self.drawn = False

    def write(self):
        for v in self.voices:
            # print(self.voices[v].notes.keys())
            n_beats = len(self.voices[v].notes.keys())
            lastnote = None
            measure = -1
            for n in range(n_beats):
                raw_note_choices = self.voices[v].notes[n]
                raw_note = list(filter(lambda x: x.selected, raw_note_choices))[0]
                raw_beat = n % self.beats_per_measure
                lookup_note = raw_note.lookup
                new_measure = False if raw_beat != 0 else True
                if new_measure:
                    measure += 1 # 0 lol
                # print(n % self.beats_per_measure, new_measure, measure)

                if lookup_note == lastnote and not new_measure:
                    self.tracks[v][-1].increment_beat()
                else:
                    # flipped = False
                    # if v in ['Bass', 'Alto']:
                    #     flipped=True
                    enharmonic = False
                    new_note = None
                    if self.song.signature.key.key == 'F#':
                        if raw_note.letter == 'C':
                            replace = Note('B#', raw_note.octave, is_bass=raw_note.is_bass,
                                 is_flipped=raw_note.is_flipped, ao_modifier=-1)
                            new_note = DrawableNote(replace, raw_beat, num_beats=1,
                                                    beat_value=self.song.signature.time.bottom, measure=measure)
                            enharmonic = True
                    if self.song.signature.key.key == 'C#':
                        if raw_note.letter == 'C':
                            replace = Note('B#', raw_note.octave, is_bass=raw_note.is_bass,
                                 is_flipped=raw_note.is_flipped, ao_modifier=-1)
                            new_note = DrawableNote(replace, raw_beat, num_beats=1,
                                                    beat_value=self.song.signature.time.bottom, measure=measure)
                            enharmonic = True
                        if raw_note.letter == 'F':
                            replace = Note('E#', raw_note.octave, is_bass=raw_note.is_bass,
                                 is_flipped=raw_note.is_flipped, ao_modifier=-1)
                            new_note = DrawableNote(replace, raw_beat, num_beats=1,
                                                    beat_value=self.song.signature.time.bottom, measure=measure)
                            enharmonic = True
                    if self.song.signature.key.key == 'Gb':
                        if raw_note.letter == 'C':
                            new_note = DrawableNote('Db', raw_beat, num_beats=1,
                                                    beat_value=self.song.signature.time.bottom, measure=measure)
                            enharmonic = True
                    if self.song.signature.key.key == 'Cb':
                        if raw_note.letter == 'C':
                            new_note = DrawableNote('Cb', raw_beat, num_beats=1,
                                                    beat_value=self.song.signature.time.bottom, measure=measure)
                            enharmonic = True
                        if raw_note.letter == 'F':
                            new_note = DrawableNote('Fb', raw_beat, num_beats=1,
                                                    beat_value=self.song.signature.time.bottom, measure=measure)
                            enharmonic = True
                    if not enharmonic:
                        new_note = DrawableNote(raw_note, raw_beat, num_beats=1,
                                                beat_value=self.song.signature.time.bottom, measure=measure)
                    # print(v, new_note, enharmonic)
                    self.tracks[v].append(new_note)
                lastnote = lookup_note

    def draw(self, filename, overwritename=None, tenor_up=True):
        pages_needed = int((self.measures + 1) / MEASURES_PER_PAGE) + 1
        pages = []
        fpdf = FPDF()
        if overwritename is not None:
            self.song.name = overwritename
        for i in range(pages_needed):
            if i == 0:
                page = utilcv2.generate_first_page(self.song, self.tracks, tenor_up)
            else:
                page = utilcv2.generate_next_page(self.song, self.tracks, i, pages_needed, tenor_up)
            pages.append(page)
            fpdf.add_page()
            cv2.imwrite(filename + '_%d' % i + '.jpg', page)
            fpdf.image(filename + '_%d' % i + '.jpg', x=0, y=0, w=200)
        fpdf.output('%s.pdf' % filename, 'F')
        self.drawn = True

    def get_first_line_of_song(self):
        if not self.drawn:
            print("Piece not drawn yet")
            return None

    def serialize(self, filename):
        obj = jsonpickle.encode(self)
        with open(filename, 'w') as ost:
            json.dump(obj, ost)

    @staticmethod
    def deserialize(filename):
        j = jsonpickle.decode(json.load(open(filename, 'r')))
        return j

    def __str__(self):
        retstr = "%d Measures" % self.measures
        retstr += '\n'
        for t in self.tracks:
            retstr += "%s:" % t
            for dn in self.tracks[t]:
                retstr += dn.__str__()
                retstr += '\n'
            retstr += '\n'
        return retstr
            