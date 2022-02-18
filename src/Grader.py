class Grader(object):

    def __init__(self, song=None, mode='default'):
        self.mode = mode
        self.song = song

    def learn(self, song):
        self.song = song

    def switch_mode(self, mode):
        self.mode = mode

    def grade(self):
        if self.mode == 'default':
            self.grade_default()

    def grade_from_file(self, file):
        pass

    def grade_default(self):
        pass
