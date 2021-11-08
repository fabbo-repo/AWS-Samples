"""
    @author: Fabián Scherle
"""
class ElicitAction(Exception):
    def __init__(self, invalid_slot, message):
        super(ElicitAction, self).__init__()
        self.invalid_slot = invalid_slot
        self.message = message

class DelegateAction(Exception):
    pass

# BAD RESPONSE, INCOMPLETE
def elicit_slot(session_attributes, intent, slot_to_elicit, message):
    response = {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'slotToElicit': slot_to_elicit,
                'type': 'ElicitSlot'
            },
            'intent': intent
        },
        'messages': [{
            'contentType': 'PlainText',
            'content': message
        }]
    }
    response['sessionState']['intent']['state'] = 'FulfillmentInProgress'
    return response


"""
    Sends a close response to lex for intent fullfillment
"""
# TESTED
def close(session_attributes, message, intent):
    response = {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent
        },
        'messages': [{
                'contentType': 'PlainText',
                'content': message
        }]
    }
    response['sessionState']['intent']['state'] = 'Fulfilled'
    return response


# UNTESTED
def delegate(session_attributes, intent):
    response = {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Delegate'
            },
            'intent': intent
        }
    }
    response['sessionState']['intent']['state'] = 'FulfillmentInProgress'
    return response
