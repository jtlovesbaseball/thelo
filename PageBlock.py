import numpy as np
import cv2
import util

#Less Magic Numbers
BLACK = 0
WHITE = 255
N_CHAN = 3
START_POINT_A = (10, 50)
START_X_B = 50
BLACK_TRI = (0, 0, 0)
TREBLE_CLIP = 22
TREBLE_START_X = 20
TREBLE_START_Y = 25
BASS_START_X   = 20
BASS_START_Y   = 150
BRACE_START_Y  = 6

#Measure sizes
MEASURE_H = 225
MEASURE_W = 300

# X Offsets
MARGIN_L = 100
MEASURE_1_END = 400
MEASURE_2_END = 700
MEASURE_3_END = 1000
MEASURE_4_END = 1300
PAGE_W = 1400

# Y Offsets
TITLE_AUTHOR = 200
TIME_INFO = 325
LINE_1_END = 550
BREAK_1_END = 600
LINE_2_END = 825
BREAK_2_END = 875
LINE_3_END = 1100
BREAK_3_END = 1150
LINE_4_END = 1375
BREAK_4_END = 1425
LINE_5_END = 1650
PAGE_H = 1864

X_LIST = [MARGIN_L, MEASURE_1_END, MEASURE_2_END, MEASURE_3_END, MEASURE_4_END]
Y_LIST = [TIME_INFO, LINE_1_END, BREAK_1_END, LINE_2_END, BREAK_2_END, LINE_3_END, 
          BREAK_3_END, LINE_4_END, BREAK_4_END, LINE_5_END]

class SubBlock(object):
    def __init__(self, parent_x0, parent_y0, parent_x1, parent_y1, name, parent=None):
        self.px0 = parent_x0
        self.px1 = parent_x1
        self.py0 = parent_y0
        self.py1 = parent_y1
        self.name = name
        self.parent = parent
        
        self.w = parent_x1 - parent_x0
        self.h = parent_y1 - parent_y0
        sub_blocks = {}     
    
    def return_draw(self, text=False, rect=True):
        a = np.zeros((self.h, self.w, N_CHAN), dtype=np.uint8)
        a[:] = WHITE
        if text:
            cv2.putText(a, self.name, START_POINT_A, fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=BLACK_TRI)
        if rect:
            cv2.rectangle(a, (1, 1), (self.w -1, self.h - 1),BLACK_TRI, thickness=2)
        return a
    
    def add_title_info(self, title, composer, original=None):
        a = np.zeros((self.h, self.w, N_CHAN), dtype=np.uint8)
        a[:] = WHITE
        cv2.putText(a, title, (START_X_B, int(self.h/3)), 
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=BLACK_TRI)
        cv2.putText(a, "Arranged w/ pyThelo by %s" % composer, (START_X_B, int(2*self.h/3)), 
                    fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=BLACK_TRI)
        if original:
            cv2.putText(a, "Original Music by %s" % original, (START_X_B, int(5*self.h/6)), 
                        fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=.75, color=BLACK_TRI)
        return a
    
    def add_time_info(self, timesig):
        a = np.zeros((self.h, self.w, N_CHAN), dtype=np.uint8)
        a[:] = WHITE
        cv2.putText(a, "%d bpm" % timesig.bpm, (START_X_B, int(self.h/3)),  fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=BLACK_TRI)
        if timesig.desc is not None:
            cv2.putText(a, "(%s)" % timesig.desc, (START_X_B + 125, int(self.h/3)), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=BLACK_TRI)
        return a
    
    def return_first_of_line(self):
        patch = np.zeros((MEASURE_H, MEASURE_W, 3), dtype=np.uint8) - 1

        treble = cv2.imread("raw/treble.png")
        bass   = cv2.imread("raw/bass.png")
        leftbrace= cv2.imread("raw/staffbracket.png")
        treble = cv2.resize(treble, (int(treble.shape[0] / 5), int(treble.shape[1] / 5)))
        treble = treble[:, TREBLE_CLIP:-TREBLE_CLIP]
        bass   = cv2.resize(bass, (int(bass.shape[0] / 12), int(bass.shape[1] / 9)))
        leftbrace = cv2.resize(leftbrace, (int(leftbrace.shape[1] / 3), int(leftbrace.shape[0] / 1.9)))
        
        patch[TREBLE_START_Y: TREBLE_START_Y + treble.shape[0], 
              TREBLE_START_X:TREBLE_START_X+treble.shape[1]] = treble
        patch[BASS_START_Y: BASS_START_Y + bass.shape[0], 
              BASS_START_X: BASS_START_X + bass.shape[1]] = bass
        patch[BRACE_START_Y: BRACE_START_Y + leftbrace.shape[0], 
              0: leftbrace.shape[1]] = leftbrace
        
        

        #treble/bass maker
        for i in range(5):
            cv2.line(patch, (20, 25 + 15*i), (300, 25 + 15*i), color =(0, 0, 0), thickness=1)
            cv2.line(patch, (20, 145+ 15*i), (300, 145 + 15*i), color =(0, 0, 0), thickness=1)
        #bass maker
        
        cv2.line(patch, (299, 25), (299, 85), color=(0, 0, 0), thickness=1)
        cv2.line(patch, (299, 145), (299, 205), color=(0, 0, 0), thickness=1)
        
        return patch
    
    def return_regular(self):
        patch = np.zeros((MEASURE_H, MEASURE_W, 3), dtype=np.uint8) - 1
        #treble/bass maker
        for i in range(5):
            cv2.line(patch, (0, 25 + 15*i), (300, 25 + 15*i), color =(0, 0, 0), thickness=1)
            cv2.line(patch, (0, 145+ 15*i), (300, 145 + 15*i), color =(0, 0, 0), thickness=1)
        cv2.line(patch, (299, 25), (299, 85), color=(0, 0, 0), thickness=1)
        cv2.line(patch, (299, 145), (299, 205), color=(0, 0, 0), thickness=1)
        return patch
    
    def return_repeat_first_of_line(self):
        patch = np.zeros((MEASURE_H, MEASURE_W, 3), dtype=np.uint8) - 1
        treble = cv2.imread("raw/treble.png")
        bass   = cv2.imread("raw/bass.png")
        leftbrace= cv2.imread("raw/staffbracket.png")

        treble = cv2.resize(treble, (int(treble.shape[0] / 5), int(treble.shape[1] / 5)))
        treble = treble[:, 22:-22]

        bass   = cv2.resize(bass, (int(bass.shape[0] / 12), int(bass.shape[1] / 9)))
        leftbrace = cv2.resize(leftbrace, (int(leftbrace.shape[1] / 3), int(leftbrace.shape[0] / 1.9)))

        patch[25:25+treble.shape[0], 20:20+treble.shape[1]] = treble
        patch[150:150+bass.shape[0], 20:20+bass.shape[1]] = bass
        patch[6:6+leftbrace.shape[0], 0:leftbrace.shape[1]] = leftbrace

        #treble/bass maker
        for i in range(5):
            cv2.line(patch, (20, 25 + 15*i), (300, 25 + 15*i), color =(0, 0, 0), thickness=1)
            cv2.line(patch, (20, 145+ 15*i), (300, 145 + 15*i), color =(0, 0, 0), thickness=1)

        #repeat is thick, thin, colon
        cv2.line(patch, (max(20+treble.shape[1], 25+bass.shape[1]), 25), (max(20+treble.shape[1], 25+bass.shape[1]), 205), 
                 color =(0, 0, 0), thickness=2)
        cv2.line(patch, (max(20+treble.shape[1], 25+bass.shape[1]) + 9, 25), (max(20+treble.shape[1], 25+bass.shape[1]) + 9, 205), 
                 color =(0, 0, 0), thickness=1)
        cv2.circle(patch, (max(20+treble.shape[1], 25+bass.shape[1]) + 16, 47), 3, (0, 0, 0), thickness=-1)
        cv2.circle(patch, (max(20+treble.shape[1], 25+bass.shape[1]) + 16, 62), 3, (0, 0, 0), thickness=-1)
        cv2.circle(patch, (max(20+treble.shape[1], 25+bass.shape[1]) + 16, 168), 3, (0, 0, 0), thickness=-1)
        cv2.circle(patch, (max(20+treble.shape[1], 25+bass.shape[1]) + 16, 184), 3, (0, 0, 0), thickness=-1)

        return patch
    
    def return_measure_end_repeat(self):
        patch = np.zeros((MEASURE_H, MEASURE_W, 3), dtype=np.uint8) - 1

        #treble/bass maker
        for i in range(5):
            cv2.line(patch, (0, 25 + 15*i), (300, 25 + 15*i), color =(0, 0, 0), thickness=1)
            cv2.line(patch, (0, 145+ 15*i), (300, 145 + 15*i), color =(0, 0, 0), thickness=1)

        cv2.line(patch, (298, 25), (298, 85), color=(0, 0, 0), thickness=2)
        cv2.line(patch, (291, 25), (291, 85), color=(0, 0, 0), thickness=2)

        cv2.line(patch, (298, 145), (298, 205), color=(0, 0, 0), thickness=2)
        cv2.line(patch, (291, 145), (291, 205), color=(0, 0, 0), thickness=2)

        cv2.circle(patch, (285, 47), 3, (0, 0, 0), thickness=-1)
        cv2.circle(patch, (285, 62), 3, (0, 0, 0), thickness=-1)
        cv2.circle(patch, (285, 168), 3, (0, 0, 0), thickness=-1)
        cv2.circle(patch, (285, 184), 3, (0, 0, 0), thickness=-1)
        return patch

class PageBlock(object):
    def __init__(self):
        self.song_name = None
        self.composer = None
        self.page = np.zeros((PAGE_H, PAGE_W, 3), dtype=np.uint8)
        self.page[:] = 255 #whiteout
        self.sub_blocks = {}
        
        #TODO NEXT- Make a create_subblock in PageBlock. We'll have every pixel taken up measure by measure 
        # (Lines are really only helpful as pixel boundaries), and fill it as needed. Drawing Measures is
        # Going to be a bitch, I'll have to fill a progress bar on them and dynamically make that large of
        # pixel out patches
        
    def generate_blank_page(self, signature=None, filename='test_out.jpg'):
        #generate L margin
        self.sub_blocks['L_MARGIN'] = SubBlock(0, 0, MARGIN_L, PAGE_H, "L_MARGIN", parent='page')
        self.sub_blocks['R_MARGIN'] = SubBlock(MEASURE_4_END, 0, PAGE_W, PAGE_H, "R_MARGIN", parent='page')
        self.sub_blocks['TITLE'] = SubBlock(MARGIN_L, 0, MEASURE_4_END, TITLE_AUTHOR, "TITLE_COMPOSER", parent='page')
        self.sub_blocks['TIME'] = SubBlock(MARGIN_L, TITLE_AUTHOR, MEASURE_4_END, TITLE_AUTHOR + 75, "Time info")
        self.sub_blocks['B_MARGIN'] = SubBlock(MARGIN_L, LINE_5_END, MEASURE_4_END, PAGE_H, "B_MARGIN", parent='page')
        
        measure = 0
        for i in range(len(Y_LIST) - 1):
            top_boundary = Y_LIST[i]
            bot_boundary = Y_LIST[i + 1]
            if i % 2 == 1:
                continue # Don't make the breaks
            for j in range(len(X_LIST) - 1):
                left_boundary = X_LIST[j]
                right_boundary = X_LIST[j + 1]
                named = 'MEASURE_%d' % measure
                
                self.sub_blocks[named] = SubBlock(left_boundary, top_boundary, right_boundary, bot_boundary, named, parent='page')
                self.sub_blocks[named + '_margin'] =  SubBlock(left_boundary, top_boundary - 50, right_boundary, top_boundary, named + '_margin', parent='page')
                
                if j == 0:
                    self.page[top_boundary:bot_boundary,
                              left_boundary:right_boundary] = self.sub_blocks[named].return_first_of_line()
                else:
                    self.page[top_boundary:bot_boundary,
                              left_boundary:right_boundary] = self.sub_blocks[named].return_regular()
                
#                 self.page[top_boundary:bot_boundary, left_boundary:right_boundary] = self.sub_blocks[named].return_draw()
                self.page[top_boundary-50:top_boundary, left_boundary:right_boundary] = self.sub_blocks[named + '_margin'].return_draw()
         
                measure += 1
                
        self.page[0:PAGE_H, 0:MARGIN_L] = self.sub_blocks['L_MARGIN'].return_draw()
        self.page[0:PAGE_H, MEASURE_4_END: PAGE_W] = self.sub_blocks['R_MARGIN'].return_draw()
        self.page[0:TITLE_AUTHOR, MARGIN_L:MEASURE_4_END] = self.sub_blocks['TITLE'].return_draw()
        self.page[TITLE_AUTHOR: TITLE_AUTHOR + 75, MARGIN_L:MEASURE_4_END] = self.sub_blocks['TIME'].return_draw()
        self.page[LINE_5_END:PAGE_H, MARGIN_L:MEASURE_4_END] = self.sub_blocks['B_MARGIN'].return_draw()
        
        cv2.imwrite(filename, self.page)
        
    def fill_with_song(self, song, write=True):
        song_title = song.name
        song_composer = song.composer
        song_signature = song.signature
        song_origin = song.original
        song_key = song_signature.key
        song_time = song_signature.time
        
        self.page[0:TITLE_AUTHOR, MARGIN_L:MEASURE_4_END] = self.sub_blocks['TITLE'].add_title_info(song_title, song_composer, song_origin)
        self.page[TITLE_AUTHOR: TITLE_AUTHOR + 75, MARGIN_L:MEASURE_4_END] = self.sub_blocks['TIME'].add_time_info(song_time)
        
        for i in range(len(Y_LIST) - 1):
            top_boundary = Y_LIST[i]
            bot_boundary = Y_LIST[i + 1]
            if i % 2 == 1:
                continue # Don't make the breaks
            for j in range(len(X_LIST) - 1):
                left_boundary = X_LIST[j]
                right_boundary = X_LIST[j + 1]
                if j > 0:
                    continue
                accidentals, n_acc = util.generate_accidentals_no_staff([MEASURE_H, MEASURE_W, 3], song_key)
                timeframe = util.generate_time_signature([MEASURE_H, MEASURE_W, 3], song_time, n_acc)

                self.page[top_boundary:bot_boundary, left_boundary:right_boundary] = cv2.bitwise_and(self.page[top_boundary:bot_boundary,
                                                                                                               left_boundary:right_boundary],
                                                                                                     accidentals)
                self.page[top_boundary:bot_boundary, left_boundary:right_boundary] = cv2.bitwise_and(self.page[top_boundary:bot_boundary,
                                                                                                               left_boundary:right_boundary],
                                                                                                     timeframe)
                
        if write:
            cv2.imwrite('test_out.jpg', self.page)
            
    def save_minisheet(self, filename, aspect=2):
        ratio = 1. / aspect
        #  leftbrace = cv2.resize(leftbrace, (int(leftbrace.shape[1] / 3), int(leftbrace.shape[0] / 1.9)))
        out = cv2.resize(self.page, (int(self.page.shape[1] / aspect), int(self.page.shape[0] / aspect)))
        cv2.imwrite(filename, out)