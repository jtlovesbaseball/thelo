class Time(object):
    def __init__(self, top, bottom, bpm):
        self.top = top
        self.bottom = bottom
        self.bpm = bpm
        
    def __str__(self):
        return "%d/%d (%d bpm)" % (self.top, self.bottom, self.bpm)