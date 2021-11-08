Python and C++ code samples using Lex V2, Polly, Transcribe and Lambda
==============================================================

* To verify that the aws cli has been installed, run the command:
~~~
aws --version
~~~

* In order to configure aws access credentials, execute:
~~~
aws configure
~~~

## Useful commands:
~~~
aws lexv2-runtime get-session --bot-id <value> --bot-alias-id <value> --locale-id <value> --session-id <value>
~~~
~~~
aws lexv2-runtime recognize-text --bot-id <value> --bot-alias-id <value> --locale-id <value> --session-id <value> --text 'Message'
~~~
~~~
aws polly synthesize-speech --output-format <value> --text <value> --voice-id <value>
~~~