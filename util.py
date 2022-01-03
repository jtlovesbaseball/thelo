import random
import numpy as np
import cv2

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
        data_file = open('raw/progressions.csv', 'r')
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
        sharps, flats = min(6, hour), 0
        patch = generate_sharps(patch, sharps)
    elif hour > 6 or 'b' in key:
        sharps, flats = 0, min(12 - hour, 6)
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
    return patch


    