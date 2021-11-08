"""
    @author: Fabián Scherle
"""
import boto3
import base64
import gzip
import os
import sys
import json
# Parent directory is added to the path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import soundCode.soundRecording as sr
import soundCode.soundPlayer as sp

# LexV2
lex = boto3.client('lexv2-runtime')
# Polly
polly = boto3.client('polly')

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Global Data:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# bot data is required for user session, it is loaded from a json file
with open('../botCredentials.json') as file:
    botCredentials = json.load(file)

BOT_ID = botCredentials['botId']
BOT_ALIAS_ID = botCredentials['botAliasId']
LOCALE_ID = botCredentials['localeId']
SESSION_ID = botCredentials['sessionId']

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Functions:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# sendTextToLex will send user input in text format to Lex V2 
# and also response will be returned in text format
def sendTextToLex(intention) :
    return lex.recognize_text(
        botId = BOT_ID,
        botAliasId = BOT_ALIAS_ID,
        localeId = LOCALE_ID,
        sessionId = SESSION_ID,
        text=intention)['messages']

# sendAudioToLex will send user input in pcm format (microphone recording)
# and it will return response in text and mp3 format
def sendAudioToLex(audio) :
    return lex.recognize_utterance(
        botId = BOT_ID,
        botAliasId = BOT_ALIAS_ID,
        localeId = LOCALE_ID,
        sessionId = SESSION_ID,
        requestContentType='audio/l16;rate=16000;channels=1',
        responseContentType='audio/mpeg',
        inputStream=audio)

# Message is compressed with gzip and encoded with base64. 
# Example of an uncompressed and unencoded message:
# '[{"content":"mensaje","contentType":"PlainText"}]'
def getMessages(code) :
    return eval( # After unzipping and decoding, it is converted to list
        (gzip.decompress(
            base64.b64decode(code)))
                .decode('utf-8'))

def sayPolly(response) :
    spoken_text = polly.synthesize_speech(Text=response,
                                        OutputFormat='mp3',
                                        VoiceId='Enrique')
    sp.playMP3(spoken_text['AudioStream'].read())
    
def close_session() :
    lex.delete_session(
        botId = BOT_ID,
        botAliasId = BOT_ALIAS_ID,
        localeId = LOCALE_ID,
        sessionId = SESSION_ID)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Test:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
print("\n\n\t\tPrimera prueba de chat:\n")
user_input = ''
while True :
    print("Escribe algo a continuación. Nota: \"record()\" para grabar audio o \"exit()\" para salir")
    print(">> ", end= '')
    user_input = input()
    
    if user_input == 'exit()' :
        try: close_session()
        except: pass
        exit()

    elif user_input == 'record()' : 
        print("Grabando > 3 segundos > ", end='')
        audio = sr.recordPCM()
        print("Fin grabacion")
        response = sendAudioToLex(audio)
        messages = getMessages(response['messages'])

        for message in messages :
            if 'content' in message :
                print("Respuesta: "+message['content'])
                sp.playMP3(response['audioStream'].read())
            else:
                print("La respuesta es una tarjeta de respuesta")

    else : 
        messages = sendTextToLex(user_input)
        if len(messages) > 0 and 'content' in messages[0] :
            response = messages[0]['content']
            print("Respuesta: "+response)
            sayPolly(response)