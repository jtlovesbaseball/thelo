import sys
sys.path.append('src/')

import cv2
import numpy as np
from Key import Key
from Time import Time
from Signature import Signature

PAGE_W = 1400
MEASURE_W = 300
CURLY_START_OFFSET = 16
ACCIDENTAL_X = 9

FINAL_LINEUP = 1365

CHORD_H = 50
MEASURE_H = 300  # Was 265
TITLE_START_X = 50
TITLE_AUTHOR = 200
TIME_INFO_HEIGHT = 75
TIME_INFO = 325
PAGE_H = 1864
PAGE_N_Y_BUFFER = 100
MEASURES_PER_PAGE = 16

MARGIN_L = 100
MARGIN_R = 1300

BLACK_TRI = (0, 0, 0)


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


def annotate_chords(measure, prev_measure_chord, w, patch):
    prev_chord = "Let there be music! (Not a chord string, wont match/print :))"
    next_chord = "Hush compiler, it will be defined in time."
    beats_per_measure = measure.n_beats
    spacing = w / beats_per_measure
    draw = False
    str_keys = True if type(list(measure.beat_chords.keys())[0]) == str else False
    for i in range(beats_per_measure):
        idx = str(i) if str_keys else i
        beat = measure.beat_chords[idx]
        if beat == 3:
            continue
        new_x, new_y = int(1 + (spacing * i)), 25
        next_chord = "%s%s" % (beat.root, beat.quality)
        abbv_chord, fontsize = abbreviate_chord(beat.root, beat.quality)

        # new_y = 16 if i % 2 == 0 else 42  # Stagger the chords when we have it every beat
        fontsize -= .41

        if prev_chord == next_chord or (i == 0 and (prev_measure_chord == next_chord)):
            draw = False
        else:
            new_y = 42 if not draw else 16  # Stagger up if we have to
            cv2.putText(patch, abbv_chord, (new_x, new_y), fontScale=fontsize, fontFace=cv2.FONT_HERSHEY_COMPLEX,
                        color=(0, 0, 0), thickness=1)
            draw = True if draw is False else False
        prev_chord = next_chord
    return patch, next_chord


def add_title_info(title, composer, original=None):
    h = TITLE_AUTHOR
    w = MARGIN_R - MARGIN_L
    a = np.zeros((h, w, 3), dtype=np.uint8)
    a[:] = 255
    cv2.putText(a, title, (TITLE_START_X, int(h / 3)),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2,
                color=BLACK_TRI)
    cv2.putText(a, "Arranged w/ pyThelo by %s" % composer,
                (TITLE_START_X, int(2 * h / 3)),
                fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1,
                color=BLACK_TRI)
    if original:
        cv2.putText(a, "Original Music by %s" % original,
                    (TITLE_START_X,  int(5 * h / 6)),
                    fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=.75,
                    color=BLACK_TRI)
    return a


def add_addtl_page_info(title, composer, pagenum, pagetotal, original=None):
    h = PAGE_N_Y_BUFFER
    w = MARGIN_R - MARGIN_L
    a = np.zeros((h, w, 3), dtype=np.uint8)
    a[:] = 255
    cv2.putText(a, title + "(pg %d/%d)" % (pagenum + 1, pagetotal), (MARGIN_L, int(h / 3)),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                color=BLACK_TRI)
    cv2.putText(a, "By %s" % composer,
                (MARGIN_L, int(2 * h / 3)),
                fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=.75,
                color=BLACK_TRI)
    if original:
        cv2.putText(a, "Original Music by %s" % original,
                    (MARGIN_L,  int(5 * h / 6)),
                    fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=.49,
                    color=BLACK_TRI)
    return a


def add_time_info(timesig):
    horiz_space = 123 if len(str(timesig.bpm)) == 2 else 145
    h = TIME_INFO_HEIGHT
    w = MARGIN_R - MARGIN_L
    a = np.zeros((h, w, 3), dtype=np.uint8)
    a[:] = 255
    cv2.putText(a, "%d bpm" % timesig.bpm,
                (TITLE_START_X, int(h/3)),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                color=BLACK_TRI)
    if timesig.desc is not None:
        cv2.putText(a, "(%s)" % timesig.desc,
                    (TITLE_START_X + horiz_space, int(h/3)),
                    fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1,
                    color=BLACK_TRI)
    return a


def generate_notes(tracks, m, beats_per_measure, tenor_up=True):

    TREBLE_DOUBLE_LEDGER = 10
    TREBLE_SINGLE_LEDGER = 25
    TREBLE_SINGLE_LEDGER_B = 115
    TREBLE_DOUBLE_LEDGER_B = 130
    TREBLE_TRIPLE_LEDGER = 145
    TREBLE_QUAD_LEDGER = 160
    BASS_DOUBLE_LEDGER_A = 140 + 25
    BASS_SINGLE_LEDGER_A = 155 + 25
    BASS_SINGLE_LEDGER = 245 + 25
    BASS_DOUBLE_LEDGER = 260 + 25

    def calculate_note_y_val(note, is_bass=True, is_treble=False):
        if is_treble:
            is_bass = False

        octave = note.octave
        order  = note.order
        full_interval = 15
        half_interval = 7.5
        octave_px = (3 * full_interval) + half_interval

        if is_bass:
            y_start = 260  + 25
            octave_score = (octave - 2) * octave_px
            order_score = half_interval * order
        else:
            y_start = 167.5  # 115 middle C + an octave for lowC
            octave_score = (octave - 3) * octave_px
            order_score = half_interval * order

        y_start -= octave_score
        y_start -= order_score
        return int(y_start)

    def calculate_note_x_offset(note, note_below=None):
        if note_below is None:
            return 0
        if note.absolute_order - note_below.absolute_order == 1:
            return 8
        if note.absolute_order - note_below.absolute_order == 0:
            if note.num_beats == note_below.num_beats:
                return 0
            return 8
        return 0

    def draw_ledger_lines(patch, x0, x1, bass, below, double, triple=False, quad=False):
        if bass:
            if below:
                cv2.line(patch, (x0, BASS_SINGLE_LEDGER),
                        (x1, BASS_SINGLE_LEDGER), BLACK_TRI, thickness=2)
                if double:
                    cv2.line(patch, (x0, BASS_DOUBLE_LEDGER),
                             (x1, BASS_DOUBLE_LEDGER), BLACK_TRI, thickness=2)
            else:
                cv2.line(patch, (x0, BASS_SINGLE_LEDGER_A),
                        (x1, BASS_SINGLE_LEDGER_A), BLACK_TRI, thickness=2)
                if double:
                    cv2.line(patch, (x0, BASS_DOUBLE_LEDGER_A),
                             (x1, BASS_DOUBLE_LEDGER_A), BLACK_TRI, thickness=2)
        else:
            if below:
                cv2.line(patch, (x0, TREBLE_SINGLE_LEDGER_B),
                        (x1, TREBLE_SINGLE_LEDGER_B), BLACK_TRI, thickness=2)
                if double:
                    cv2.line(patch, (x0, TREBLE_DOUBLE_LEDGER_B),
                             (x1, TREBLE_DOUBLE_LEDGER_B), BLACK_TRI, thickness=2)
            else:
                cv2.line(patch, (x0, TREBLE_SINGLE_LEDGER),
                        (x1, TREBLE_SINGLE_LEDGER), BLACK_TRI, thickness=2)
                if double:
                    cv2.line(patch, (x0, TREBLE_DOUBLE_LEDGER),
                             (x1, TREBLE_DOUBLE_LEDGER), BLACK_TRI, thickness=2)
        if triple:
            cv2.line(patch, (x0, TREBLE_TRIPLE_LEDGER),
                     (x1, TREBLE_TRIPLE_LEDGER), BLACK_TRI, thickness=2)
        if quad:
            cv2.line(patch, (x0, TREBLE_QUAD_LEDGER),
                     (x1, TREBLE_QUAD_LEDGER), BLACK_TRI, thickness=2)
        return patch

    def draw_note(patch, note, x, y, v):
        stem_offset_x = -8 if v in ['B', 'A'] else 8
        stem_offset_y = 52 if v in ['B', 'A'] else -52
        note_center_x = x
        note_center_y = y
        BLACK_TRI = (0, 0, 0)
        if v == 'A':
            note.is_bass = False
            BLACK_TRI = (0, 0, 255)
        if v == 'S':
            BLACK_TRI = (147, 20, 255)
        if v == 'T':
            BLACK_TRI = (255, 0, 0)
        if note.num_beats == 4:
            cv2.circle(patch, (note_center_x, note_center_y), 8, BLACK_TRI, 2)
        if note.num_beats == 3:
            cv2.circle(patch, (note_center_x, note_center_y), 8, BLACK_TRI, 2)
            cv2.line(patch, (note_center_x + stem_offset_x, note_center_y),
                     (note_center_x + stem_offset_x, note_center_y + stem_offset_y),
                     BLACK_TRI, 2)
            cv2.circle(patch, (note_center_x + 14, note_center_y + 4), 3, BLACK_TRI, -1)
        if note.num_beats == 2:
            cv2.circle(patch, (note_center_x, note_center_y), 8, BLACK_TRI, 2)
            cv2.line(patch, (note_center_x + stem_offset_x, note_center_y),
                     (note_center_x + stem_offset_x, note_center_y + stem_offset_y),
                     BLACK_TRI, 2)
        if note.num_beats == 1:
            cv2.circle(patch, (note_center_x, note_center_y), 8, BLACK_TRI, -1)
            cv2.line(patch, (note_center_x + stem_offset_x, note_center_y),
                     (note_center_x + stem_offset_x, note_center_y + stem_offset_y),
                     BLACK_TRI, 2)
        return patch

    patch = np.zeros([MEASURE_H, MEASURE_W, 3], dtype=np.uint8) - 1
    gap = MEASURE_W - 10
    gap_dist = int(gap / beats_per_measure)
    first_note_start = 15
    beat_dist = 35
    x_offset_from_ledger = 10
    below = {}

    for bpm in range(beats_per_measure):
        below[bpm] = None
    prev_abs = -1
    for v in ["B",  "A", "T", "S"]:
        voice_notes_in_m = [t for t in tracks[v] if t.in_measure(m)]
        for note in voice_notes_in_m:
            this_beat = note.start_beat
            start_x = first_note_start + (this_beat * gap_dist)
            end_x = start_x + beat_dist
            note_center_x = start_x + x_offset_from_ledger + \
                            calculate_note_x_offset(note, below[this_beat])
            note_center_y = -3
            is_bass = True
            if v == 'T':
                is_bass = note.bass  # False if note.absolute_order > 14 else True #16 D?

            if v == 'A':
                # is_bass = True if note.absolute_order < 14 else False
                is_bass = False
            if v == 'S':
                is_bass = False
            note_center_y = calculate_note_y_val(note, is_bass=is_bass)

            if note.absolute_order < 4 and is_bass:
                if note.absolute_order < 2 and is_bass:
                    patch = draw_ledger_lines(patch, start_x, end_x,
                                              True, True, True)
                else:
                    patch = draw_ledger_lines(patch, start_x, end_x,
                                              True, True, False)

            if note.absolute_order > 14 and is_bass:
                if note.absolute_order > 16 and is_bass:
                    patch = draw_ledger_lines(patch, start_x, end_x,
                                              True, False, True)
                else:
                    patch = draw_ledger_lines(patch, start_x, end_x,
                                              True, False, False)

            if note.absolute_order < 18 and not is_bass:
                if note.absolute_order < 16 and not is_bass:
                    patch = draw_ledger_lines(patch, start_x, end_x,
                                              False, True, True)
                else:
                    patch = draw_ledger_lines(patch, start_x, end_x,
                                              False, True, False)

            if note.absolute_order > 28 and not is_bass:
                if note.absolute_order > 30 and not is_bass:
                    patch = draw_ledger_lines(patch, start_x, end_x,
                                              False, False, True)
                else:
                    patch = draw_ledger_lines(patch, start_x, end_x,
                                              False, False, False)

            if note.absolute_order <= 13 and v == 'T' and tenor_up:
                patch = draw_ledger_lines(patch, start_x, end_x,
                                          False, True, True, True, False)
            if note.absolute_order <= 11 and v == 'T' and tenor_up:
                patch = draw_ledger_lines(patch, start_x, end_x,
                                          False, True, True, True, True)
            if v == 'A':
                note.is_bass = False
            patch = draw_note(patch, note, note_center_x, note_center_y, v)
            below[this_beat] = note
    return patch


def generate_first_page(song, tracks, tenor_up=True):
    page = np.zeros((PAGE_H, PAGE_W, 3), dtype=np.uint8)
    page[:] = 255  # whiteout

    song_title = song.name
    song_composer = song.composer
    song_signature = song.signature
    song_origin = song.original
    song_key = song_signature.key
    song_time = song_signature.time
    song_measure = song.measures
    tracks = tracks

    prev_chord = "undefined"

    page[0:TITLE_AUTHOR, MARGIN_L:MARGIN_R] = \
        add_title_info(song_title, song_composer, song_origin)
    page[TITLE_AUTHOR: TITLE_AUTHOR + TIME_INFO_HEIGHT,
        MARGIN_L:MARGIN_R] = add_time_info(song_time)

    sig_size_time, sig_size_no = calculate_signature_size(song_signature)

    perfect_fourline_x_ending = MARGIN_L + sig_size_no + (4 * MEASURE_W)
    x_offset = max(0, 100 - (perfect_fourline_x_ending - FINAL_LINEUP))
    x_offset_first = FINAL_LINEUP - (3 * MEASURE_W) - sig_size_time

    music_start_y = TITLE_AUTHOR + TIME_INFO_HEIGHT

    standard_dims = [MEASURE_H, MEASURE_W, 3]

    # Main measure makin loop
    final_measure = False
    for m in range(len(song_measure)):
        note_img = generate_notes(tracks, m, song_signature.time.top, tenor_up)
        if m > MEASURES_PER_PAGE - 2:
            break
        if m == 0:
            measure = make_first_measure_of_piece(standard_dims,
                                                  song_signature, m)
        elif m % 4 == 3: # Indented one newline on third
            measure = make_first_measure_of_line(standard_dims,
                                                 song_signature, m)
        elif m == len(song_measure) - 1:
            measure = make_final_measure(standard_dims)
            final_measure = True

        elif m % 4 == 3: #Gotta put the right line ender on
            measure = make_generic_measure(standard_dims)
        else:
            measure = make_generic_measure(standard_dims)

        line_num = int((m + 1) / 4)
        y0 = music_start_y + (line_num * (standard_dims[0] + CHORD_H)) + CHORD_H
        y1 = y0 + standard_dims[0]

        if m < 3:
            x_starts = {0: x_offset_first,
                        1: x_offset_first + (1 * standard_dims[1]) + sig_size_time,
                        2: x_offset_first + (2 * standard_dims[1]) + sig_size_time}
            x_ends = {0: x_starts[1], 1: x_starts[2], 2: x_starts[2] + standard_dims[1]}
            x0, x1 = x_starts[m], x_ends[m]
        else:
            new_start = x_offset
            new_end = x_offset + sig_size_no + standard_dims[1]
            if m % 4 == 3:
                x0, x1 = new_start, new_end
            else:
                measures_added_from_first = m % 4
                x0 = new_end + (measures_added_from_first * standard_dims[1])
                x1 = new_end + ((measures_added_from_first + 1) * standard_dims[1])
        if final_measure:
            x1 += 10
        # print(m, x0, y0, x1, y1)
        # str_keys = True if type(list(song_measure.keys())[0]) == str else False
        # m = str(m) if str_keys else m
        chord_annotation, prev_chord = annotate_chords(song_measure[m], prev_chord, MEASURE_W,
                                                       page[y0-50:y0, x1-300:x1])
        page[y0-50:y0, x1-300:x1] = chord_annotation
        page[y0: y1, x0:x1] = measure
        page[y0:y1, x1-MEASURE_W:x1] = cv2.bitwise_and(page[y0:y1, x1-MEASURE_W:x1], note_img)
        # Overlay the notes directly here. [y0:y1, x1-MEASURE_W:x1]
        cv2.line(page, (x1, y0 + 40), (x1, y0 + 230 + 25), color=(0, 0, 0), thickness=1)
    return page


def generate_next_page(song, tracks, pagenum, pagetotal, tenor_up=True):
    page = np.zeros((PAGE_H, PAGE_W, 3), dtype=np.uint8)
    page[:] = 255  # whiteout
    prev_chord = "undefined"

    song_title = song.name
    song_composer = song.composer
    song_signature = song.signature
    song_origin = song.original
    song_key = song_signature.key
    song_time = song_signature.time
    song_measure = song.measures
    final_idx = len(song_measure) - 1
    start_measure = (MEASURES_PER_PAGE - 1) + ((pagenum - 1) * MEASURES_PER_PAGE)

    page[0:PAGE_N_Y_BUFFER, MARGIN_L:MARGIN_R] = \
        add_addtl_page_info(song_title, song_composer, pagenum, pagetotal, song_origin)

    sig_size_time, sig_size_no = calculate_signature_size(song_signature)

    perfect_fourline_x_ending = MARGIN_L + sig_size_no + (4 * MEASURE_W)
    x_offset = max(0, 100 - (perfect_fourline_x_ending - FINAL_LINEUP))
    music_start_y = PAGE_N_Y_BUFFER

    standard_dims = [MEASURE_H, MEASURE_W, 3]

    # Main measure makin loop
    final_measure = False
    i = 0
    for m in range(MEASURES_PER_PAGE):
        song_measure_n = start_measure + m
        note_img = generate_notes(tracks, song_measure_n, song_signature.time.top, tenor_up)

        if m % 4 == 0:
            measure = make_first_measure_of_line(standard_dims,
                                                 song_signature, song_measure_n)
        elif m == final_idx:
            measure = make_final_measure(standard_dims)
            final_measure = True
        else:
            measure = make_generic_measure(standard_dims)

        line_num = int(m / 4)
        # if i % 4 == 3:
        #     line_num -= 1  # Fourth one getting dragged?
        y0 = music_start_y + (line_num * (standard_dims[0] + CHORD_H)) + CHORD_H
        y1 = y0 + standard_dims[0]

        new_start = x_offset
        new_end = x_offset + sig_size_no + standard_dims[1]
        if i % 4 == 0:
            x0, x1 = new_start, new_end
        else:
            measures_added_from_first = max((i - 1) % 4, 0)
            x0 = new_end + (measures_added_from_first * standard_dims[1])
            x1 = new_end + ((measures_added_from_first + 1) * standard_dims[1])
        if final_measure:
            x1 += 10

        chord_annotation = "Undefined"
        if song_measure_n == len(song_measure):  # This may need to happen earlier? Onlya problem here
            break
        else:
            chord_annotation, prev_chord = annotate_chords(song_measure[song_measure_n], prev_chord, MEASURE_W,
                                                           page[y0-50:y0, x1-300:x1])
        page[y0-50:y0, x1-300:x1] = chord_annotation
        page[y0: y1, x0:x1] = measure
        page[y0:y1, x1-MEASURE_W:x1] = cv2.bitwise_and(page[y0:y1, x1-MEASURE_W:x1], note_img)
        cv2.line(page, (x1, y0 + 40), (x1, y0 + 230), color=(0, 0, 0), thickness=1)
        i += 1
    return page


def calculate_signature_size(signature):
    measure = create_curlybrace(MEASURE_H)
    return (insert_keysignature(measure, signature, MEASURE_H, 69, time=True).shape[1],
            insert_keysignature(measure, signature, MEASURE_H, 69, time=False).shape[1])


def create_curlybrace(h):
    leftbrace = cv2.imread("raw/staffbracket.png")
    leftbrace = cv2.resize(leftbrace, (int(leftbrace.shape[1] / 4), int(leftbrace.shape[0] / 1.65)))
    measure = np.zeros((h, leftbrace.shape[1], 3), dtype=np.uint8) - 1
    measure[CURLY_START_OFFSET: CURLY_START_OFFSET + leftbrace.shape[0],
    0:leftbrace.shape[1]] = leftbrace
    return measure


def create_clef_image(h):
    treble = cv2.imread("raw/treble.png")
    bass = cv2.imread("raw/bass.png")
    treble = cv2.cvtColor(cv2.resize(treble, (int(treble.shape[0] / 5), int(treble.shape[1] / 5))),
                          cv2.COLOR_BGR2RGB)
    treble = treble[:, 22:-22]
    bass = cv2.resize(bass, (int(bass.shape[0] / 12), int(bass.shape[1] / 9)))

    max_w = max(treble.shape[1], bass.shape[1]) + 4
    patch = np.zeros([h, max_w, 3], dtype=np.uint8) - 1

    patch[40:40 + treble.shape[0], 2:2 + treble.shape[1]] = treble
    patch[175 + 25:175 + 25 + bass.shape[0], 2:2 + bass.shape[1]] = bass
    return patch


def make_regular_measure_end(h, openleft=False):
    patch = np.zeros([h, MEASURE_W, 3], dtype=np.uint8) - 1
    for i in range(5):
        cv2.line(patch, (0, 40 + 15 * i), (MEASURE_W, 40 + 15 * i), color=(0, 0, 0), thickness=1)
        cv2.line(patch, (0, 170 + 25 + 15 * i), (MEASURE_W, 170 + 25 + 15 * i), color=(0, 0, 0), thickness=1)
    if not openleft:
        cv2.line(patch, (0, 40), (0, 230 + 25), color=(0, 0, 0), thickness=1)
    cv2.line(patch, (300, 40), (300, 230 + 25 + 25), color=(0, 0, 0), thickness=1)
    return patch


def make_staff(patch, left=True, right=False):
    # Shift down bass lef 25 pixels from 170 -> 190
    w = patch.shape[1]
    for i in range(5):
        cv2.line(patch, (0, 40 + 15 * i), (patch.shape[1], 40 + 15 * i), color=(0, 0, 0), thickness=1)
        cv2.line(patch, (0, 170 + 25 + 15 * i), (patch.shape[1], 170 + 25 + 15 * i), color=(0, 0, 0), thickness=1)
    if left:
        cv2.line(patch, (0, 40), (0, 230 + 25), color=(0, 0, 0), thickness=1)
    if right:
        cv2.line(patch, (w - 1, 40), (w - 1, 230 + 25), color=(0, 0, 255), thickness=2)
    return patch


def create_accidentals(signature, h):
    hour = 0

    key = signature.key.key
    tonality = signature.key.tonality

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

    flats, sharps = 0, 0
    if hour < 6 or '#' in key:
        sharps, flats = hour, 0
    if hour > 6 or key in ['Gb', 'Cb']:
        sharps, flats = 0, 12 - hour
    if key == 'C#':
        sharps = 7
        flats = 0
    if hour == 6:
        if key == 'F#':
            sharps, flats = 6, 0
        else:
            sharps, flats = 0, 6

    accidentals = max(flats, sharps)
    needed_w = 8 + (accidentals * ACCIDENTAL_X)
    dims = [h, needed_w, 3]
    patch = np.zeros(dims, dtype=np.uint8) - 1

    if sharps > flats:
        patch = generate_sharps(patch, accidentals)
    elif flats > sharps:
        patch = generate_flats(patch, accidentals)
    else:
        if key == 'Gb':  # This is at the bottom of the enharmonic circle. I like sharps more than flats, this can be changed via arg.
            patch = generate_flats(patch, accidentals)
        else:
            patch = generate_sharps(patch, accidentals)

    return patch


def insert_keysignature(measure, signature, h, measure_number, time):  # Two parter
    clef_image = create_clef_image(h)
    clef_image = make_staff(clef_image)
    cv2.putText(clef_image, "%d" % measure_number, (clef_image.shape[1] - 36, 36),
                fontScale=1.5, fontFace=cv2.FONT_HERSHEY_PLAIN, color=(0, 0, 0), thickness=2)
    acci_image = create_accidentals(signature, h)
    acci_image = make_staff(acci_image, left=False)
    if time:
        time_image = insert_timesignature(signature, h)
        time_image = make_staff(time_image, left=False)
        measure = np.concatenate((measure, clef_image, acci_image, time_image), axis=1)
    else:
        measure = np.concatenate((measure, clef_image, acci_image), axis=1)
    return measure


def insert_timesignature(signature, h):  # Two parter
    top, bottom = signature.time.top, signature.time.bottom
    lentop, lenbot = len(str(top)), len(str(bottom))
    width = 49 if (lentop > 1 or lenbot > 1) else 25
    patch = np.zeros([h, width, 3], dtype=np.uint8) - 1
    cv2.putText(patch, "%s" % top, (0, 65), fontScale=1.25, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0),
                thickness=2)
    cv2.putText(patch, "%s" % bottom, (0, 95), fontScale=1.25, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0),
                thickness=2)
    cv2.putText(patch, "%s" % top, (0, 195 + 25), fontScale=1.25, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0),
                thickness=2)
    cv2.putText(patch, "%s" % bottom, (0, 230 + 25), fontScale=1.25, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0),
                thickness=2)
    return patch


def generate_sharps(patch, sharps):
    i = 0
    sharp_ys = [(45, 190 + 25), (65, 213 + 25), (39, 182 + 25), (61, 203 + 25),
                (79, 227 + 25), (50, 199 + 25), (74, 220 + 25)]
    # sharp_ys = [(45, 190), (65, 213), (39, 182), (61, 203), (79, 227), (50, 199), (74, 220)]
    # sharp_ys = [(30, 165), (50, 188), (24, 155), (46, 180), (64, 200), (35, 170), (59, 190)]
    while sharps > 0:
        x = 0 + (i * ACCIDENTAL_X)
        treble_y, bass_y = sharp_ys[i]
        cv2.putText(patch, "#", (x, treble_y), fontScale=.75, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0),
                    thickness=2)
        cv2.putText(patch, "#", (x, bass_y), fontScale=.75, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0),
                    thickness=2)
        sharps -= 1
        i += 1
    return patch


def generate_flats(patch, flats):
    i = 0
    flat_ys = [(75, 194 + 25), (54, 173 + 25), (84, 204 + 25), (59, 180 + 25),
               (90, 210 + 25), (69, 190 + 25), (95, 220 + 25)]
    # flat_ys = [(75, 194), (54, 173), (84, 204), (59, 180), (90, 210), (69, 190), (95, 220)]
    # flat_ys = [(60, 194), (39, 173), (69, 204), (44, 180), (75, 210), (54, 190), (80, 217)]
    while flats > 0:
        x = 0 + (i * ACCIDENTAL_X)
        treble_y, bass_y = flat_ys[i]
        cv2.putText(patch, "b", (x, treble_y), fontScale=.64, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0),
                    thickness=1)
        cv2.putText(patch, "b", (x, bass_y), fontScale=.64, fontFace=cv2.FONT_HERSHEY_COMPLEX, color=(0, 0, 0),
                    thickness=1)
        flats -= 1
        i += 1
    return patch


def make_first_measure_of_piece(dims, signature, measure_number):
    # create canvas of size dims. The x is dimensions of BAR AFTER ALL SIGNATURE
    measure = create_curlybrace(h=dims[0])
    measure = insert_keysignature(measure, signature, h=dims[0], measure_number=measure_number, time=True)  # Two parter
    time = insert_timesignature(signature, h=dims[0])
    body = make_regular_measure_end(h=dims[0], openleft=True)
    measure = np.concatenate((measure, body), axis=1)
    return measure


def make_first_measure_of_line(dims, signature, measure_number):
    # create canvas of size dims. The x is dimensions of BAR AFTER ALL SIGNATURE
    measure = create_curlybrace(h=dims[0])
    measure = insert_keysignature(measure, signature, h=dims[0], measure_number=measure_number,
                                  time=False)  # Two parter
    body = make_regular_measure_end(h=dims[0], openleft=True)
    measure = np.concatenate((measure, body), axis=1)
    return measure


def make_generic_measure(dims):
    body = make_regular_measure_end(h=dims[0], openleft=False)
    return body


def make_final_measure(dims):
    body = make_generic_measure(dims)
    tail = np.zeros((body.shape[0], 10, 3), dtype=np.uint8) - 1
    tail = make_staff(tail, right=True)
    fin = np.concatenate((body, tail), axis=1)
    return fin


if __name__ == '__main__':
    k = Key('C#', 'major')
    t = Time(4, 4, 69, descriptor="With gusto")
    s = Signature(k, t)

    dims = [MEASURE_H, MEASURE_W, 3]
    measure = make_first_measure_of_piece(dims, s, 0)

    print("Notes start at %d" % (measure.shape[1] - MEASURE_W))
