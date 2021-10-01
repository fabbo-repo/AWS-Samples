"""
    @author: Fabián Scherle
"""
import boto3
import os
import sys
import json

# bot data is required for user session, it is loaded from a json file
with open('../botCredentials.json') as file:
    botCredentials = json.load(file)

# Parent directory is added to the path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import soundCode.soundRecording as sr
import soundCode.soundPlayer as sp

# LexV2 client uses 'lexv2-runtime'
client = boto3.client('lexv2-runtime')

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

print('Playing response...')

sp.playMP3(response['audioStream'].read())

"""
{
    'ResponseMetadata': 
    {
        'RequestId': 'bbd50cf9-a2ac-40c2-a8e8-4a229712caed', 
        'HTTPStatusCode': 200, 
        'HTTPHeaders':
        {
            'x-amzn-requestid': 'bbd50cf9-a2ac-40c2-a8e8-4a229712caed', 
            'x-amz-lex-input-mode': 'Text', 
            'x-amz-lex-interpretations': 'H4sIAAAAAAAAAJWQMQvCMBCF/8vNpbSCIq5ixUUER3GI6VWC1wskVxBK/rtJdWscuh3vfXw87jYC07C33JkWWSPsRvDaunjUZRUKMCzIkmJWfUzh6BDF8PP0LQrwZMVHIMJelCSmGagzRNjGWie365UYy9dff7aMEEIxzvWNInoo/ZrrJ/7f2Kqst7m1h7c4tdy1ybkuzraDltVy3Tqnm56Rc90/behozJUBAAA=', 
            'x-amz-lex-messages': 'H4sIAAAAAAAAAIuuVkrOzytJzStRslLyyM9JVNKBCYRUFqQCBQNyEjPzQlIrSpRqYwETXjd0LgAAAA==', 
            'x-amz-lex-session-id': 'test_session', 
            'x-amz-lex-session-state': 'H4sIAAAAAAAAAC3NQQ6CMBCF4bvMGhJsNAI7Y6Jh40JPMLQDmaRMlQ4LQ7i7rbr+/ry3gmP0YTxZ5SDQrqDvJ0ELZx8iwVYAi5JoFsEpy3UmUpax+0EB0QeNKUhxVNTcXBY/sPfkEtsgA88T5oPH329BvuNh5pEF89ydXgtF7VzivneHyg5NiQZtua+sKbGmutyjMc1xZyym5e0Dd0CzmrwAAAA=', 
            'date': 'Mon, 27 Sep 2021 11:14:49 GMT', 
            'content-type': 'audio/mpeg', 
            'transfer-encoding': 'chunked'
        }, 
        'RetryAttempts': 0
    }, 
    'inputMode': 'Text', 
    'contentType': 'audio/mpeg', 
    'messages': 'H4sIAAAAAAAAAIuuVkrOzytJzStRslLyyM9JVNKBCYRUFqQCBQNyEjPzQlIrSpRqYwETXjd0LgAAAA==', 
    'interpretations': 'H4sIAAAAAAAAAJWQMQvCMBCF/8vNpbSCIq5ixUUER3GI6VWC1wskVxBK/rtJdWscuh3vfXw87jYC07C33JkWWSPsRvDaunjUZRUKMCzIkmJWfUzh6BDF8PP0LQrwZMVHIMJelCSmGagzRNjGWie365UYy9dff7aMEEIxzvWNInoo/ZrrJ/7f2Kqst7m1h7c4tdy1ybkuzraDltVy3Tqnm56Rc90/behozJUBAAA=', 
    'sessionState': 'H4sIAAAAAAAAAC3NQQ6CMBCF4bvMGhJsNAI7Y6Jh40JPMLQDmaRMlQ4LQ7i7rbr+/ry3gmP0YTxZ5SDQrqDvJ0ELZx8iwVYAi5JoFsEpy3UmUpax+0EB0QeNKUhxVNTcXBY/sPfkEtsgA88T5oPH329BvuNh5pEF89ydXgtF7VzivneHyg5NiQZtua+sKbGmutyjMc1xZyym5e0Dd0CzmrwAAAA=', 
    'sessionId': 'test_session', 
    'audioStream': <botocore.response.StreamingBody object at 0x000002BAE82C0EB0>
}
"""