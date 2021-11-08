"""
    @author: Fabián Scherle
"""
import boto3
import os
import sys
import time
# Parent directory is added to the path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import soundCode.soundPlayer as sp

# API: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html

fecha = time.strftime("%d-%m-%y")
print(fecha)
hora = time.strftime("%I:%M%p")
print(hora)

polly = boto3.client('polly')

spoken_text = polly.synthesize_speech(
    Engine='standard',  # not rquired
    OutputFormat='mp3',
    Text='<speak>La fecha de hoy es,  <say-as interpret-as="date" format="ddmmyyyy" detail="1">'+str(fecha)+'</say-as></speak>',
    TextType='ssml',    # not rquired
    VoiceId='Enrique')
sp.playMP3(spoken_text['AudioStream'].read())

spoken_text = polly.synthesize_speech(
    Engine='standard',  # not rquired
    OutputFormat='mp3',
    Text='<speak>y la hora es, <say-as interpret-as="time" format="hms12">'+str(hora)+'</say-as></speak>',
    TextType='ssml',    # not rquired
    VoiceId='Enrique')
sp.playMP3(spoken_text['AudioStream'].read())