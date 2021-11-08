# C++ code samples using Lex V2
=============================

Code samples implemented in C++, using AWS Lex V2. 
* The botCredentials.json file contains the data needed to establish a session with the bot.

> It is necessary to install additional libraries:
~~~
sudo apt install libjsoncpp-dev
~~~

## SDK API:
* [lexv2-runtime](https://sdk.amazonaws.com/cpp/api/LATEST/class_aws_1_1_lex_runtime_v2_1_1_lex_runtime_v2_client.html)

## Compile and execute:
~~~
g++ <path> -ldl -laws-cpp-sdk-lexv2-runtime -laws-cpp-sdk-core -ljsoncpp -o binario
./binario
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