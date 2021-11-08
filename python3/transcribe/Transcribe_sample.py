"""
    @author: Fabián Scherle
"""
import time
import boto3

transcribe = boto3.client('transcribe')

job_name = "transcript-for-lex"
job_uri = "s3://input.mp3"
transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat='mp3',
    LanguageCode='es-ES'
)
while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(1)
print(status)