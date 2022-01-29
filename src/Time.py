class Time(object):
    def __init__(self, top, bottom, bpm, swing=False, descriptor=None):
        self.top = top
        self.bottom = bottom
        self.bpm = bpm
        self.swing = swing
        self.desc = descriptor
        
    def __str__(self):
        return "%d/%d (%d bpm)" % (self.top, self.bottom, self.bpm)