import numpy as np
import cv2

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
        
    def generate_subblocks(self, subblocks):
        pass
        
        
    def populate_self(self, drawable):
        """
        It would be mayhem if i overloaded the method methinks, so this is when we can
        draw something, generate_sub is to create subblocks
        """
        pass
    
    def return_draw(self):
        a = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        a[:] = 255
        cv2.putText(a, self.name, (10, 50), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=(255, 20, 0))
        cv2.rectangle(a, (1, 1), (self.w -1, self.h - 1), (0, 0, 0), thickness=2)
        return a

class PageBlock(object):
    def __init__(self, name, composer):
        self.song_name = name
        self.composer = composer
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
                self.page[top_boundary:bot_boundary, left_boundary:right_boundary] = self.sub_blocks[named].return_draw()
                
                self.sub_blocks[named + '_margin'] =  SubBlock(left_boundary, top_boundary - 50, right_boundary, top_boundary, named + '_margin', parent='page')
                self.page[top_boundary-50:top_boundary, left_boundary:right_boundary] = self.sub_blocks[named + '_margin'].return_draw()

                
                
                measure += 1
                
        self.page[0:PAGE_H, 0:MARGIN_L] = self.sub_blocks['L_MARGIN'].return_draw()
        self.page[0:PAGE_H, MEASURE_4_END: PAGE_W] = self.sub_blocks['R_MARGIN'].return_draw()
        self.page[0:TITLE_AUTHOR, MARGIN_L:MEASURE_4_END] = self.sub_blocks['TITLE'].return_draw()
        self.page[TITLE_AUTHOR: TITLE_AUTHOR + 75, MARGIN_L:MEASURE_4_END] = self.sub_blocks['TIME'].return_draw()
        self.page[LINE_5_END:PAGE_H, MARGIN_L:MEASURE_4_END] = self.sub_blocks['B_MARGIN'].return_draw()
        
        cv2.imwrite(filename, self.page)
    
    def populate_page(self, measures):
        #fill song title
        #fill composer info
        #fill thelo plugs subtly
        #populate 4 lines
        pass
        
    