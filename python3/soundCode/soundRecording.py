from numpy import int16
import sounddevice as sd
from scipy.io.wavfile import write
import pickle

def recordPCM(seconds = 3, fs = 16000) :
    # fs Sample rate
    # seconds = 3  # Duration of recording
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype=int16)
    sd.wait()  # Wait until recording is finished
    return pickle.dumps(myrecording)

def saveRECtoWAV(pcm, path = 'temp.wav', fs = 16000) :
    write(path, fs, pcm)