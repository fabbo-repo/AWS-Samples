Python code samples using Lex V2, Polly and Transcribe
=======================================================

Examples of code implemented in Python3, using AWS Lex V2, AWS Polly, and AWS Transcribe services. 
* In the soundCode package there are files with .py extension that will be used by the sample files in the "lexV2", "polly" and "transcribe" packages. 
* In the case of "transcribe" it is necessary to have s3 permissions and add the respective path in the corresponding line. 
* The botCredentials.json file contains the data needed to establish a session with the bot.

> It is necessary to install additional libraries:
    ~~~python
    pip install -r requirements.txt
    ~~~
> or update them:
    ~~~python
    pip install --upgrade -r requirements.txt
    ~~~

## boto3 API:
* [lexv2-runtime](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-runtime.html)
* [polly](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html)
* [Transcribe](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe.html)

## Dependencies:
* boto3
* awscli
* pygame
* pydub
* sounddevice
* scipy
* ffmpeg
* avconv
* boto3-stubs[lexv2-runtime]
* mypy-boto3-lexv2-models
* pvrecorder

## Useful commands:

    aws lexv2-runtime get-session --bot-id <value> --bot-alias-id <value> --locale-id <value> --session-id <value>

    aws lexv2-runtime recognize-text --bot-id <value> --bot-alias-id <value> --locale-id <value> --session-id <value> --text 'Message'

    aws polly synthesize-speech --output-format <value> --text <value> --voice-id <value>