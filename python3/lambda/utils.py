"""
    @author: Fabián Scherle
"""

import logging
import json
# import datetime
import dateutil.parser
import lex_utils

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

"""
    Generates brand options for each product type.
"""
def generate_product_options(product):
    car_brands = ['audi', 'kia', 'ford', 'hyundai', 'citroen']
    
    if product.lower() in ["coche", "auto", "carro"] :
        return ", ".join(car_brands)
    else :
        return "ninguna marca"

"""
    Checks if the produt is a car, phone or tablet
"""
def isvalid_product(product):
    valid_products = ['coche', 'carro', 'auto', 'celular', 'movil', 'tablet']
    return product.lower() in valid_products

"""
   Check if the date is real
"""
def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False

"""
    validate_slots is responsible of the validation of the slots.
    If any are invalid, return a dictionary with the invalid slot
"""
def validate_slots(slots) :
    product_slot = slots['ProductSlot']
    # another_slot = slots['SlotName']

    product = product_slot['value']['originalValue']

    if product_slot and not isvalid_product(product):
        return {
            'isValid': False,
            'invalidSlot': product_slot
        }
        
    # Sample for checking dates
    #if checkin_date:
    #    if not isvalid_date(checkin_date):
    #        return build_validation_result(False, 'CheckInDate', 'I did not understand your check in date.  When would you like to check in?')
    #    if datetime.datetime.strptime(checkin_date, '%Y-%m-%d').date() <= datetime.date.today():
    #        return build_validation_result(False, 'CheckInDate', 'Reservations must be scheduled at least one day in advance.  Can you try a different date?')

    return { 'isValid': True }

"""
    init_or_load_session will load the product slot as a session attribute
    and will maintain the session data or attributes, in case there is one.
"""
def init_or_load_session(event):
    current_intent = event['sessionState']['intent']
    # product_slot will contain the product that the user has sent to lex
    product_slot = current_intent['slots']['ProductSlot']['value']['originalValue']
    
    # If there are no sessionAttributes field, it will be defined
    try: session_attributes = event['sessionAttributes']
    except: session_attributes = {}
    
    # currentProduct field for session data is created for future interactions or improvements
    session_attributes['currentProduct'] = product_slot
    return session_attributes

"""
    Clear/update session with final attributes
    Before the intention is fullfilled
"""
def finalize_session(session_attributes):
    product = session_attributes.pop('currentProduct', None)
    session_attributes['lastProductRequested'] = product

"""
    validate_dialog uses validate_slots and checks session attributes.
    If any are invalid, re-elicit for their value
"""
def validate_dialog(slots, session_attributes):
    # slots are chacked
    validation_result = validate_slots(slots)
    if not validation_result['isValid'] :
        invalid_slot = validation_result['invalidSlot']
        # re-elicit invalid slot
        raise lex_utils.ElicitAction(
            invalid_slot=invalid_slot,
            message='Actualmente no soportamos {} como producto valido, que otro producto desea?'.format(invalid_slot)
        )
    
