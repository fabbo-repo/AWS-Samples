"""
    @author: Fabián Scherle
"""
import boto3
import os
import sys
import json
import gzip
import base64
import time

# bot data is required for user session, it is loaded from a json file
with open('../botCredentials.json') as file:
    botCredentials = json.load(file)

# Parent directory is added to the path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import soundCode.soundRecording as sr
import soundCode.soundPlayer as sp


# Message is compressed with gzip and encoded with base64. 
# Example of an uncompressed and unencoded message:
# '[{"content":"mensaje","contentType":"PlainText"}]'
def getMessage(code) :
    return eval( # After unzipping and decoding, it is converted to list
        (gzip.decompress(
            base64.b64decode(code)))
                .decode('utf-8'))


# LexV2 client uses 'lexv2-runtime'
client = boto3.client('lexv2-runtime')
polly = boto3.client('polly')


print('Recording for 3 seconds...')
audio = sr.recordPCM()
print('Sending record...')

# Record is sent
response = client.recognize_utterance(
    botId = botCredentials['botId'],
    botAliasId = botCredentials['botAliasId'],
    localeId = botCredentials['localeId'],
    sessionId = botCredentials['sessionId'],
    requestContentType='audio/l16; rate=16000; channels=1',
    responseContentType='audio/mpeg',
    inputStream=audio
)

# inputTranscript contains the recognition of the recording, passed to text, 
# compressed with gzip and encoded with base64
recognized_text = getMessage(response["inputTranscript"])
print("--> Texto reconocido: " + recognized_text)

# Content of inputTranscript is sent to polly
spoken_text = polly.synthesize_speech(
    Engine='standard',  # not rquired
    OutputFormat='mp3',
    Text=recognized_text,
    TextType='text',    # not rquired
    VoiceId='Enrique')

sp.playMP3(spoken_text['AudioStream'].read())

client.delete_session(
    botId = botCredentials['botId'],
    botAliasId = botCredentials['botAliasId'],
    localeId = botCredentials['localeId'],
    sessionId = botCredentials['sessionId'])



# Recognized text is saved in a file
fecha = time.strftime("%d-%m-%y")
hora = time.strftime("%I:%M%p")
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'lexV2.txt')
with open(path, "a") as data:
    data.write(" -> ".join([fecha, hora, recognized_text]) + "\n")