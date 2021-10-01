from os import remove
from pygame import mixer

def playMP3(mp3) :
    with open('temp.mp3','wb') as f:
        f.write(mp3)
        f.close()
    mixer.init()
    mixer.music.load('temp.mp3')
    mixer.music.play()
    while mixer.music.get_busy() :
        pass
    mixer.quit()
    remove('temp.mp3')