"""
    @author: Fabián Scherle
"""
import boto3
import os
import sys
import json
# Parent directory is added to the path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
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
# sendLex will send user input to Lex V2 and response will be returned 
def sendLex(intention) :
    messages = lex.recognize_text(
        botId = BOT_ID,
        botAliasId = BOT_ALIAS_ID,
        localeId = LOCALE_ID,
        sessionId = SESSION_ID,
        text=intention)['messages']
    return messages

# sayPolly takes care of the TTS function 
# (Lex V2 audioStream is ignored in this example)
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
    print("Escribe algo a continuación, \"exit()\" para salir")
    user_input = input()
    if user_input == 'exit()' : 
        try: close_session()
        except: pass
        exit()
    
    messages = sendLex(user_input)
    if len(messages) > 0 and 'content' in messages[0] :
        response = messages[0]['content']
        print("Respuesta: "+response)
        sayPolly(response)

