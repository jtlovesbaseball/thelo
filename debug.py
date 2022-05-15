import sys
sys.path.append('src/')

from Song import Song
from Key import Key
from Time import Time
from Signature import Signature
from Composer import Composer
from Piece import Piece
from Grader import Grader
from IPython.display import Image

# Creating the Key Signature, and Time Signature
SONG_TITLE = 'song0.json'
PIECE_TITLE = 'piece0.json'
k = Key(key='C', tonality='major')
t = Time(top=4, bottom=4, bpm=69, descriptor="Nice")
s = Signature(key=k, time=t)

# Initializing a song with the signature given above, and generating 1000 random chords
# Chord Progressions must be valid resolutions/deceptions
song_0 = Song("Random Chord Voicings in %s %s" % (k.key, k.tonality), 'JT', s)
song_0.generate_chords(n=69)

composer_0 = Composer()
composer_0.learn(song_0)
piece_0 = composer_0.compose_fourvoice(method='first')
piece_0.draw("song_0", overwritename="1st Inv Chord Voicings in %s %s" % (k.key, k.tonality), tenor_up=False)

##############################

song_0.serialize(SONG_TITLE)
song_1 = Song.deserialize(SONG_TITLE)
print(song_0.__str__() == song_1.__str__())

snoop = Grader(piece=piece_0)
song_1_score = snoop.grade()
