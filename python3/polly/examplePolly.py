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
    Text='Hola, soy Enrique.',
    TextType='text',    # not rquired
    VoiceId='Enrique')

sp.playMP3(spoken_text['AudioStream'].read())


"""
{
    'ResponseMetadata': 
    {
        'RequestId': '19da0d5b-465f-4078-92d4-8337c78436c5', 
        'HTTPStatusCode': 200, 
        'HTTPHeaders': 
        {
            'x-amzn-requestid': '19da0d5b-465f-4078-92d4-8337c78436c5', 
            'x-amzn-requestcharacters': '18', 
            'content-type': 'audio/pcm', 
            'transfer-encoding': 'chunked', 
            'date': 'Tue, 28 Sep 2021 08:17:54 GMT'
        }, 
        'RetryAttempts': 0
    }, 
    'ContentType': 'audio/pcm', 
    'RequestCharacters': '18', 
    'AudioStream': <botocore.response.StreamingBody object at 0x000002364154B5B0>
}
"""