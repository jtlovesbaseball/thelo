from Note import DrawableNote
import util2 as utilcv2
import cv2
from fpdf import FPDF

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
                    new_note = DrawableNote(raw_note, raw_beat, num_beats=1, 
                                            beat_value=self.song.signature.time.bottom, measure=measure)
                    # print(new_note.measure, n % self.beats_per_measure)
                    self.tracks[v].append(new_note)
                lastnote = lookup_note

    def draw(self, filename):
        pages_needed = int((self.measures + 1) / MEASURES_PER_PAGE) + 1
        pages = []
        fpdf = FPDF()
        for i in range(pages_needed):
            if i == 0:
                page = utilcv2.generate_first_page(self.song, self.tracks)
            else:
                page = utilcv2.generate_next_page(self.song, self.tracks, i, pages_needed)
            pages.append(page)
            fpdf.add_page()
            cv2.imwrite(filename + '_%d' % i + '.jpg', page)
            fpdf.image(filename + '_%d' % i + '.jpg', x=0, y=0, w=200)
        fpdf.output('%s.pdf' % filename, 'F')

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
            