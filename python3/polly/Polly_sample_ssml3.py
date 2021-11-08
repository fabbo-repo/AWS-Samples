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
    Text='<speak>En vez de decir casa puedo decir, <say-as interpret-as="characters">casa</say-as></speak>',
    TextType='ssml',    # not rquired
    VoiceId='Enrique')
sp.playMP3(spoken_text['AudioStream'].read())