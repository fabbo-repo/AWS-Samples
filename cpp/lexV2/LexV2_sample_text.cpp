#include <aws/core/Aws.h>
#include <aws/core/utils/Outcome.h>
#include <aws/core/auth/AWSCredentialsProvider.h>
#include <aws/lexv2-runtime/LexRuntimeV2Client.h>
#include <aws/lexv2-runtime/model/RecognizeTextRequest.h>
#include <aws/lexv2-runtime/model/DeleteSessionRequest.h>
#include <jsoncpp/json/value.h>
#include <jsoncpp/json/reader.h>
#include <jsoncpp/json/json.h>
#include <fstream>

std::string m_bot_id;
std::string m_bot_alias_id;
std::string m_bot_locale_id;
std::string m_session_id;
Aws::LexRuntimeV2::LexRuntimeV2Client *m_lexRuntime;


int loadCredentials(std::string path) {
    std::ifstream jsonFile(path);
    if (!jsonFile.is_open()) {
        std::cout << "Error openning file" << std::endl;
        return -1;
    }
    std::string line; std::string lines;
    while (std::getline(jsonFile, line)) {
        // skip empty lines
        if ( line == "" ) continue;
        else lines += line;
    }
    jsonFile.close();

    Json::Value botCredentials;
    Json::Reader reader;
    bool succesJson = reader.parse(lines, botCredentials); // reader can also read strings
    if(!succesJson){
        std::cout << "Error parsing json" << std::endl;
        return -1;
    }

    m_bot_id = botCredentials["botId"].asString();
    m_bot_alias_id = botCredentials["botAliasId"].asString();
    m_bot_locale_id = botCredentials["localeId"].asString();
    m_session_id = botCredentials["sessionId"].asString();
    return 0;
}


Aws::Vector<Aws::LexRuntimeV2::Model::Message> recognizeText(std::string text) {
    Aws::LexRuntimeV2::Model::RecognizeTextRequest textRequest;
    textRequest.SetBotId(m_bot_id);
    textRequest.SetBotAliasId(m_bot_alias_id);
    textRequest.SetLocaleId(m_bot_locale_id);
    textRequest.SetSessionId(m_session_id);
    textRequest.SetText(text);
    
    return m_lexRuntime->RecognizeText(textRequest).GetResult().GetMessages();
}


void deleteSession() {
    Aws::LexRuntimeV2::Model::DeleteSessionRequest delSessRequest;
    delSessRequest.SetBotId(m_bot_id);
    delSessRequest.SetBotAliasId(m_bot_alias_id);
    delSessRequest.SetLocaleId(m_bot_locale_id);
    delSessRequest.SetSessionId(m_session_id);
    m_lexRuntime->DeleteSession(delSessRequest);
}


int main(int argc, char* argv[])
{
    Aws::SDKOptions options;
    options.loggingOptions.logLevel = Aws::Utils::Logging::LogLevel::Trace;
    // Oppening and creating API files, processes and sockets
    Aws::InitAPI(options);

    // credentials and config are loaded from aws directory
    m_lexRuntime = new Aws::LexRuntimeV2::LexRuntimeV2Client;
    
    // Bot credentials are loaded from a json file
    if(loadCredentials("../botCredentials.json"))
        exit(-1);
    
    std::cout << "Request message: Hola" << std::endl;
    Aws::Vector<Aws::LexRuntimeV2::Model::Message> messages = recognizeText("Hola");
    std::cout << "Number of responses: " << messages.size() << std::endl;
    for (int i = 0; i < messages.size(); i++ )
        std::cout << "Response message N" << i << ": " 
            << messages.at(i).GetContent().data() << std::endl;

    // Session is recommended to be deleted
    deleteSession();

    // Closing API files, processes and sockets
    Aws::ShutdownAPI(options);

    return 0;
}

