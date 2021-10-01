"""
    @author: Fabián Scherle
"""
import boto3
import json

# LexV2 client uses 'lexv2-runtime'
client = boto3.client('lexv2-runtime')

# bot data is required for user session, it is loaded from a json file
with open('../botCredentials.json') as file:
    botCredentials = json.load(file)

response = client.recognize_text(
    botId = botCredentials['botId'],
    botAliasId = botCredentials['botAliasId'],
    localeId = botCredentials['localeId'],
    sessionId = botCredentials['sessionId'],
    text='Hola')

print("Pregunta: Hola")
if 'messages' in response and len(response['messages']) > 0 :
    print("Respuesta: " + response['messages'][0]['content'])

client.delete_session(
    botId = botCredentials['botId'],
    botAliasId = botCredentials['botAliasId'],
    localeId = botCredentials['localeId'],
    sessionId = botCredentials['sessionId'])
