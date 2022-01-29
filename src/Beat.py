class Beat(object):
    # I think I will need this for things more than quarter notes
    def __init__(self, note):
        self.notes = [note]
        self.fraction = [1]
    
    def get_singlenote(self):
        return self.notes[0]
    
    def __lt__(self, o):
        return self.get_singlenote() < o.get_singlenote()
    
    def __eq__(self, o):
        return self.get_singlenote() == o.get_singlenote()
