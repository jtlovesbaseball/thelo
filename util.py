import random

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
            
    