"""
    @author: Fabián Scherle
"""

import logging
import lex_utils
import utils

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.debug('event.bot.name=%s', event['bot']['name'])
    logger.debug('intentName=%s', event['sessionState']['intent']['name'])
    logger.debug('messageVersion=%s', event['messageVersion'])

    intent_name = event['sessionState']['intent']['name']

    if intent_name == 'TestLambda': 
        return testLambda(event)
    # elif (add more intents here)
    else:
        raise Exception('Intención con nombre %s no es válida' % intent_name)


def testLambda(event):
    # Create currentProduct attribute
    session_attributes = utils.init_or_load_session(event)
    intent = event['sessionState']['intent']
    slots = event['sessionState']['intent']['slots']

    try : utils.validate_dialog(slots, session_attributes)
    except lex_utils.ElicitAction as ea :
        # request a new value, re-elicit
        return lex_utils.elicit_slot(
            session_attributes,
            intent,
            ea.invalid_slot,  # elicit this invalid slot
            ea.message   # with this custom message
        )
    except lex_utils.DelegateAction :
        # tell Lex to move on with the next slot
        return lex_utils.delegate(session_attributes, slots)

    product = session_attributes['currentProduct']
    response_options = utils.generate_product_options(product)
    
    # Session attributes are modified
    utils.finalize_session(session_attributes)
    
    return lex_utils.close(
        session_attributes,
        'Tenemos '+product+' de '+response_options+'',
        event['sessionState']['intent']
    )