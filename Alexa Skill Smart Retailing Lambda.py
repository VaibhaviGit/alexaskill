#------------------------------Part1--------------------------------
# declaration
Shop_LIST = ["vegetable shop", "g mart", "fresh india"]
Item_List = {"sugar":"60 bucks",
"salt" : "25 bucks",
"potato" : "30 bucks",
"tomato" : "50 bucks",
"cake":"80 bucks",
"bread":"90 bucks",
"rice": "200 bucks"
    
}
Shop_DETAILS = {"vegetable shop":"potato and tomato",

"g mart":"sugar, salt and rice",

"fresh india":"cheese cake and bread"
}
#------------------------------Part2--------------------------------
# Here we define our Lambda function and configure what it does when 
# an event with a Launch, Intent and Session End Requests are sent. # The Lambda function responses to an event carrying a particular 
# Request are handled by functions such as on_launch(event) and 
# intent_scheme(event).
def lambda_handler(event, context):
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()
#------------------------------Part3--------------------------------
# Here we define the Request handler functions
def on_start():
    print("Session Started.")

def on_launch(event):
    onlunch_MSG = "Hi, welcome to the smart shopping Alexa Skill. your nearest stores are: " + ', '.join(map(str, Shop_LIST)) + ". "\
    "If you would like to hear more about a particular shop, you could say for example: Get me itemlist for g mart?"
    reprompt_MSG = "Do you want to hear more about a particular store?"
    card_TEXT = "Pick a Store."
    card_TITLE = "Choose a store."
    return output_json_builder_with_reprompt_and_card(onlunch_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def on_end():
    print("Session Ended.")
#-----------------------------Part3.1-------------------------------
# The intent_scheme(event) function handles the Intent Request. 
# Since we have a few different intents in our skill, we need to 
# configure what this function will do upon receiving a particular 
# intent. This can be done by introducing the functions which handle 
# each of the intents.
def intent_scheme(event):
    
    intent_name = event['request']['intent']['name']

    if intent_name == "getretailer":
        return storedetail(event)   
    elif intent_name == "placeorder":
        return orderplaced(event)
    elif intent_name == "getprice":
        return price2(event)
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)
#---------------------------Part3.1.1-------------------------------
# Here we define the intent handler functions

def storedetail(event):
    name=event['request']['intent']['slots']['retailer']['value']
    if name.lower() in Shop_LIST:
        msg="The available items are: "+Shop_DETAILS.get(name.lower())+". To get price for any item you can say like what is price of sugar?"
        assistance_MSG=msg
        reprompt_MSG="Do you want to hear more about a particular store"
        card_TEXT="Store found"
        card_TITLE="Store found"
        return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
    else:
        msg2="Incorrect store. Please chose correct store. "
        assistance_MSG=msg2
        reprompt_MSG="Do you want to hear more about a particular store"
        card_TEXT="Incorrect Store"
        card_TITLE="Incorrect Store"
        return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)


def orderplaced(event):
    name=event['request']['intent']['slots']['order']['value']
    itemname=event['request']['intent']['slots']['items']['value']
    if name.lower() in Shop_LIST and itemname.lower() in Shop_DETAILS.get(name.lower()):
        assistance_MSG="Thank you for shopping with us. Your Order is placed successfully. You will get an sms on registered mobile number soon"
        reprompt_MSG="Do you want to hear more about a particular store?"
        card_TEXT="Order found"
        card_TITLE="Order found"
        return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
    else:
        assistance_MSG="Incorrect Order"
        reprompt_MSG="Do you want to hear more about a particular store?"
        card_TEXT="Incorrect Order"
        card_TITLE="Incorrect Order"
        return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
        
def price2(event):
    name=event['request']['intent']['slots']['prices']['value']
    if name.lower() in Item_List:
        msg="The price is: "+Item_List.get(name.lower())+" To place order you can say like place order for g mart for the item sugar"
        assistance_MSG=msg
        reprompt_MSG="Do you want to hear more about a particular store?"
        card_TEXT="Items found"
        card_TITLE="Items found"
        return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
    else:
        assistance_MSG="Incorrect Item"
        reprompt_MSG="Do you want to hear more about store items?"
        card_TEXT="Incorrect Item"
        card_TITLE="Incorrect Item"
        return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
        
def stop_the_skill(event):
    stop_MSG = "Thank you. Bye!"
    reprompt_MSG = ""
    card_TEXT = "Bye."
    card_TITLE = "Bye Bye."
    return output_json_builder_with_reprompt_and_card(stop_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)
    
def assistance(event):
    assistance_MSG = "You can choose among these shops: " + ', '.join(map(str, Shop_LIST)) 
    reprompt_MSG = "Do you want to hear more about a particular store?"
    card_TEXT = "You've asked for help."
    card_TITLE = "Help"
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def fallback_call(event):
    fallback_MSG = "I can't help you with that, try rephrasing the question or ask for help by saying HELP."
    reprompt_MSG = "Do you want to hear more about a particular store?"
    card_TEXT = "You've asked a wrong question."
    card_TITLE = "Wrong question."
    return output_json_builder_with_reprompt_and_card(fallback_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
#------------------------------Part4--------------------------------
# The response of our Lambda function should be in a json format. 
# That is why in this part of the code we define the functions which 
# will build the response in the requested format. These functions
# are used by both the intent handlers and the request handlers to 
# build the output.
def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict

def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict
    
def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict    

def response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeach_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict

def output_json_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value)
    return response_dict