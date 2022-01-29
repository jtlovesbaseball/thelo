class Signature(object):
    def __init__(self, key, time):
        self.key = key
        self.time = time
        
    def __str__(self):
        retstr = """Key: %s, Time: %s""" % (self.key.simple_str(), self.time.__str__())
        return retstr