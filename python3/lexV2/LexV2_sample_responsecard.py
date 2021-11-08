"""
    @author: Fabián Scherle
"""
import boto3
import os
import sys
import json
import gzip
import base64
# Parent directory is added to the path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import soundCode.soundRecording as sr

# bot data is required for user session, it is loaded from a json file
with open('../botCredentials.json') as file:
    botCredentials = json.load(file)


# LexV2 client uses 'lexv2-runtime'
client = boto3.client('lexv2-runtime')

# Message is compressed with gzip and encoded with base64. 
# Example of an uncompressed and unencoded message:
# '[{"content":"mensaje","contentType":"PlainText"}]'
def getMessage(code) :
    return eval( # After unzipping and decoding, it is converted to list
        (gzip.decompress(
            base64.b64decode(code)))
                .decode('utf-8'))

print('Recording for 3 seconds...')
audio = sr.recordPCM()
print('Sending record...')

response = client.recognize_utterance(
    botId = botCredentials['botId'],
    botAliasId = botCredentials['botAliasId'],
    localeId = botCredentials['localeId'],
    sessionId = botCredentials['sessionId'],
    requestContentType='audio/l16; rate=16000; channels=1',
    responseContentType='audio/mpeg',
    inputStream=audio
)

client.delete_session(
    botId = botCredentials['botId'],
    botAliasId = botCredentials['botAliasId'],
    localeId = botCredentials['localeId'],
    sessionId = botCredentials['sessionId'])

message = getMessage(response['messages'])
if len(message) > 0 and 'imageResponseCard' in message[0] :
    print('Tarjeta de respuesta:')
    print('\tTitulo: '+str(message[0]['imageResponseCard']['title']))
