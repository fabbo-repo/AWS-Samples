"""
    @author: Fabián Scherle
"""
import boto3
import os
import sys
# Parent directory is added to the path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import soundCode.soundPlayer as sp

# API: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html

polly = boto3.client('polly')

spoken_text = polly.synthesize_speech(
    Engine='standard',  # not rquired
    OutputFormat='mp3',
    Text='<speak> Otra forma de decir 1 es decir <say-as interpret-as="ordinal">1</say-as></speak>',
    TextType='ssml',    # not rquired
    VoiceId='Enrique')
sp.playMP3(spoken_text['AudioStream'].read())

spoken_text = polly.synthesize_speech(
    Engine='standard',  # not rquired
    OutputFormat='mp3',
    Text='<speak> y 58 es decir <say-as interpret-as="ordinal">58</say-as></speak>',
    TextType='ssml',    # not rquired
    VoiceId='Enrique')
sp.playMP3(spoken_text['AudioStream'].read())


spoken_text = polly.synthesize_speech(
    Engine='standard',  # not rquired
    OutputFormat='mp3',
    Text='<speak> por ultimo digo 1 2 3 4 5 como <say-as interpret-as="cardinal">12345</say-as></speak>',
    TextType='ssml',    # not rquired
    VoiceId='Enrique')
sp.playMP3(spoken_text['AudioStream'].read())