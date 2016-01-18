from flask import Flask, request
from twilio.rest import TwilioRestClient
from model.message import Message, ResponseBuilder
from model.actions import ActionBuilder
from model.error import ActionError

app = Flask(__name__)

ACCOUNT_SID = "AC04675359e5f5e5ca433a2a5c17e9ddf6"
AUTH_TOKEN = "ea3bc3ef80b8a7283d26eb94426518c8"
SERVER_NUMBER = "+13126989087"


@app.route('/', methods=['GET', 'POST'])
def index():
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    if request.method == 'POST':
        ''' Parse request store as message '''
        message = Message(From=request.form["From"],
                          To=request.form["To"],
                          Body=request.form["Body"],
                          Picture=request.form["Picture"],
                          id=request.form["MessageSid"])
        message.put()

        ''' Pass message into action builder.'''
        try:
            ab = ActionBuilder(message)
            action_key, action = ab.make_action()
            rb = ResponseBuilder(action_key, action)
            response_num_list, response = rb.build_response()
        except ActionError as message:
            response_num_list = [action.attacker]
            response = "[ERR] {}".format(message)
        except:
            response_num_list = [action.attacker]
            response = "[ERR] Unknown Error"

        for response_number in response_num_list:
            '''Make message'''
            outgoing_message = Message(From=SERVER_NUMBER,
                                       To=response_number,
                                       Body=response)
            outgoing_message.put()

            '''Send message'''
            client.messages.create(
                to=response_number,
                from_=SERVER_NUMBER,
                body=response)

    return "Samsu Assassins Running!"


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
