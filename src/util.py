import random
import numpy as np
import cv2
import json
from Note import Note
from Beat import Beat

TREBLE_W = 46
TREBLE_OFFSET = 25
ACCIDENTAL_DISTANCE = 9

sharp_ys = [
    (30, 165),
    (50, 188),
    (24, 155),
    (46, 180),
    (64, 200),
    (35, 170),
    (59, 190)
]

flat_ys = [
    (60, 194),
    (39, 173),
    (69, 204),
    (44, 180),
    (75, 210),
    (54, 190),
    (80, 217)
]

class MajorChordTransition(object):
    def __init__(self):
        data_file = open('raw/progressions_nonself.csv', 'r')
        self.transit_hash = {}
        for line in data_file:
            st_line = line.strip()
            to, fr, pr = st_line.split(',')
            if to not in self.transit_hash:
                self.transit_hash[to] = {}
            self.transit_hash[to][fr] = float(pr)
        
    def transition(self, fr, to=None):
        if to is not None:
            return to
        transitors = self.transit_hash[fr]
        for transit in transitors:
            trial = random.random()
            if trial < self.transit_hash[fr][transit]:
                return transit
        return fr # no joy


def generate_sharps(patch, sharps):
    i = 0
    while sharps > 0:
        x = TREBLE_W + TREBLE_OFFSET + (i * ACCIDENTAL_DISTANCE)
        treble_y, bass_y = sharp_ys[i]
        cv2.putText(patch, "#", (x, treble_y), fontScale=.75, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0), thickness=2)
        cv2.putText(patch, "#", (x, bass_y), fontScale=.75, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0), thickness=2)
        sharps -= 1
        i += 1
    return patch
        

def generate_flats(patch, flats):
    i = 0
    while flats > 0:
        x = TREBLE_W + TREBLE_OFFSET + (i * ACCIDENTAL_DISTANCE)
        treble_y, bass_y = flat_ys[i]
        cv2.putText(patch, "b", (x, treble_y), fontScale=.64, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0), thickness=1)
        cv2.putText(patch, "b", (x, bass_y), fontScale=.64, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0), thickness=1)
        flats -= 1
        i += 1
    return patch
    
    
def generate_accidentals_no_staff(dims, keysig, fsharp_over_gflat=True):
    """
    In order to deal with enharmonics on the circle of fifths, we need to represent it as a circle, and modulate away after
    tonality math to modify accidentals
    """
    patch = np.zeros(dims, dtype=np.uint8) - 1
    hour = 0
    key = keysig.key
    tonality = keysig.tonality
    
    if key == 'G':
        hour = 1
    if key == 'D':
        hour = 2
    if key == 'A':
        hour = 3
    if key == 'E':
        hour = 4
    if key == 'B' or key == 'Cb':
        hour = 5
    if key == 'F#' or key == 'Gb':
        hour = 6
    if key == 'C#' or key == 'Db':
        hour = 7
    if key == 'Ab':
        hour = 8
    if key == 'Eb':
        hour = 9
    if key == 'Bb':
        hour = 10
    if key == 'F':
        hour = 11
        
    if tonality == 'minor':
        hour += 9
    hour %= 12

    if hour < 6 or '#' in key:
        #sharps, flats = min(6, hour), 0
        sharps, flats = hour, 0
        patch = generate_sharps(patch, sharps)
    elif hour > 6 or 'b' in key:
        #sharps, flats = 0, min(12 - hour, 6)
        sharps, flats = 0, 12 - hour
        patch = generate_flats(patch, flats)
    else:
        if not fsharp_over_gflat: # This is at the bottom of the enharmonic circle. I like sharps more than flats, this can be changed via arg.
            sharps, flats = 0, 6
            patch = generate_flats(patch, flats)
        else:
            sharps, flats = 6, 0
            patch = generate_sharps(patch, sharps)        
    return patch, max(flats, sharps)

def generate_time_signature(dims, song_time, n_acc):
    patch = np.zeros(dims, dtype=np.uint8) - 1
    ACCIDENTAL_OFFSET = (1 * ACCIDENTAL_DISTANCE) * (n_acc + 0)
    TOTAL_OFFSET = TREBLE_OFFSET + ACCIDENTAL_OFFSET + 55
    top = song_time.top
    bottom = song_time.bottom
    cv2.putText(patch, "%s" % top, (TOTAL_OFFSET, 50), fontScale=1.25, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0), thickness=2)
    cv2.putText(patch, "%s" % bottom, (TOTAL_OFFSET, 80), fontScale=1.25, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0), thickness=2)
    cv2.putText(patch, "%s" % top, (TOTAL_OFFSET, 170), fontScale=1.25, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0), thickness=2)
    cv2.putText(patch, "%s" % bottom, (TOTAL_OFFSET, 205), fontScale=1.25, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0), thickness=2)
    cv2.line(patch, (TOTAL_OFFSET + 25, 0), (TOTAL_OFFSET + 25, 255), thickness=1, color=(0, 0, 255))
    return patch, TOTAL_OFFSET + 25


def generate_chord_annotations(measure, x0, x1, y0, y1, prev_measure_chord, fourvoice):
    def abbreviate_chord(chord, quality):
        prefix = chord
        suffix = ""
        size = 1
        if quality == 'minor':
            suffix = 'min'
            size = 1
        elif quality == 'dim':
            suffix = 'dim'
            size = 1
        elif quality == "aug":
            suffix = "+"
        return "%s%s" % (prefix, suffix), size
    
    dims = [y1 - y0, x1 - x0, 3]
    patch = np.zeros(dims, dtype=np.uint8) - 1
    width = x1 - x0
    beats_per_measure = measure.n_beats
    spacing = width / beats_per_measure
    prev_chord = "Income tax is illegal"
    for i in range(beats_per_measure):
        beat = measure.beat_chords[i]
        if beat == 3:
            continue
        new_x, new_y = int(1 + (spacing * i)), 25
        next_chord = "%s%s" %(beat.root, beat.quality)
        abbv_chord, fontsize = abbreviate_chord(beat.root, beat.quality)
        
        if fourvoice:
            new_y = 16 if i % 2 == 0 else 42 # Stagger the chords when we have it every beat
            fontsize -= .41
        if prev_chord == next_chord or (i == 0 and prev_measure_chord == next_chord):
            pass
        else:
            cv2.putText(patch, abbv_chord, (new_x, new_y), fontScale=fontsize, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0), thickness=1)
        prev_chord = next_chord
    return patch, next_chord
      
class NoteEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Note):
            return {'letter': o.letter, 'octave': o.octave, 'is_bass': o.is_bass, 
                    'lookup': o.lookup, 'selected': o.selected, 'unselected': o.unselected}
        return super(NoteEncoder, self).default(o)
    
class BeatEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Beat):
            return {'fraction': o.fraction, 'notes': json.dumps(o.notes, cls=NoteEncoder)}
#             returndict[
#             for i in range(len(o.notes)):
#                 re
#                 returndict['letter_%d' % i] = o.notes[i].letter
#                 returndict['octave_%d' % i] = o.notes[i].octave
#                 returndict['is_bass_%d' % i] = o.notes[i].is_bass
#                 returndict['lookup_%d'] = o.notes[i].lookup
#                 returndict['selected_%d'] = 
        return super(BeatEncoder, self).default(o)
    