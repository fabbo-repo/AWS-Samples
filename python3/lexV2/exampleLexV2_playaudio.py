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

# LexV2 client uses 'lexv2-runtime'
client = boto3.client('lexv2-runtime')

# bot data is required for user session, it is loaded from a json file
with open('../botCredentials.json') as file:
    botCredentials = json.load(file)

response = client.recognize_utterance(
    botId = botCredentials['botId'],
    botAliasId = botCredentials['botAliasId'],
    localeId = botCredentials['localeId'],
    sessionId = botCredentials['sessionId'],
    requestContentType='text/plain; charset=utf-8',
    responseContentType='audio/mpeg',
    inputStream='Hola'
)

client.delete_session(
    botId = botCredentials['botId'],
    botAliasId = botCredentials['botAliasId'],
    localeId = botCredentials['localeId'],
    sessionId = botCredentials['sessionId'])

sp.playMP3(response['audioStream'].read())
