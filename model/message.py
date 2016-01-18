from google.appengine.ext import ndb
from model.player import Player


class Message(ndb.Model):
    '''
    Message object.
    Key: TwilMessageid
    Fields:
        From phone number
        To Phone number
        Body raw message body
        Picture image string
    '''
    From = ndb.StringProperty()
    To = ndb.StringProperty()
    Body = ndb.StringProperty()
    Picture = ndb.StringProperty(default="")


class ResponseBuilder(object):
    def __init__(self, action_key, action):
        self.action_key = action_key
        self.action = action
        numbers_qry = Player.query()
        all_keys = numbers_qry.fetch(keys_only=True)
        self.all_numbers = [key.id() for key in all_keys]

    def build_response(self):
        command = self.action.action
        if command == "KILL":
            return self._kill()

    def _kill(self):
        if self.action.need_validation:
            response_number = [self.action.victim]
            response = "[REPLY {}] Were you recently killed? Reply 'Y' or 'N'.".format(self.action_key)
        else:
            response_number = [self.all_numbers]
            victim = Player.get_by_id(self.action.victim)
            response = "{} has been killed".format(victim.id())
        return response_number, response
