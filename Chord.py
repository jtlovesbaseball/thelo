class Chord(object):
    """
    Why do we need a chord object?
    
    Because chords in music take some amount of bars / measures. They'll have a function depending on their key,
    (Tonic, Subdom, dom), but that's going to be difficult to determine for my level of musis knowledge right now. Passing
    in the key/tonality as a place holder s.t. it can be determined.
    """
    
    SEVEN_NAMES = ["root", "3rd", "5th", "7th"]
    
    def __init__(self, notes, parent_key, quality, n_measures=2, inversion=0):
        self.notes = notes
        self.inversion = inversion
        self.root = self.notes[0]
        self.quality = quality
        self.n = n_measures
        self.n_remaining = n_measures
        
        self.SEVEN_NAMES = ["root", " 3rd", " 5th", " 7th"]
        
        # Each time theres an inversion, pop the root and play it as the top
        for inv in range(inversion):
            if self.notes[1] in ['#', 'b', 'bb']:
                pass
            newlist = self.notes[1:]
            newlist.extend(self.notes[0])
            if newlist[-1] in ['#', 'b']:
                newlist[-2] = '%s%s' % (newlist[-2], newlist[-1])
                newlist = newlist[:-1]
            self.notes = newlist
        
    
    def __str__(self):
        chordstr = ""
        for i in range(len(self.notes)):
            chordstr += '%s: %s | ' % (self.SEVEN_NAMES[i], self.notes[i])
        chordstr = chordstr[:-3] if '|' in chordstr else chordstr
        retstr = """Chord: %s %s %s (%d measure) %s """ % (self.root, self.quality, '(Inversion %d)' % self.inversion if self.inversion != 0 else '(Root Position)', self.n ,chordstr)
        return retstr
            
        