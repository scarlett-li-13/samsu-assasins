from google.appengine.ext import ndb
from player import Player
from datetime import datetime


class ActionBuilder(object):
    '''Action builder which takes a message object and returns ActionObject.'''
    action = Action()

    def __init__(self, message):
        self.message = message

    def make_action(self):
        action, params = self._get_command()
        self._get_attacker()

        if action == "KILL":
            return self._kill(), self.action()
        else:
            raise ActionError("CMD", action)

    def _get_command(self):
        message_body = self.message.Body.split()
        action = message_body.pop(0)
        params = message_body
        return action, params

    def _get_attacker(self):
        self.attacker = Player.get_by_id(self.message.From)

    def _get_victim(self, victim_name):
        potential_victims = Player.query(Player.codename == victim_name).fetch()
        for i, victim in enumerate(potential_victims):
            if i > 0:
                raise ActionError("NAME", victim_name)
            self.victim = victim
        raise ActionError("NAME", victim_name)

    def _kill(self):
        if self._validate_kill():
            ''' Invalid kill '''
            return
        self.action.attacker = self.attacker.key.id()
        self.action.action = "KILL"
        self.action.victim = self.victim.id()
        self.action.datetime = datetime.now()
        self.action.need_validation = True
        return self.action.put()

    def _validate_kill(self):
        my_team = self.attacker.key.parent()
        my_target = my_team.kill
        victim_team = self.victim.key.parent()
        if my_target != victim_team.id():
            raise ActionError("TEAM", "")

        if self.attacker.state == "DEAD":
            raise ActionError("ME", self.attacker.state)

        if self.victim.state != "ALIVE":
            raise ActionError("THEM", self.victim.state)

        return False


class Action(ndb.Model):
    '''
    Action object
    Key: default assigned by NDB
    Fields:
        attacker - phone number
        action - string
        victim - phone number
        datetime
        place
        validation
    '''
    attacker = ndb.StringProperty(required=True)
    action = ndb.StringProperty(require=True,
                                choices=set(["KILL",
                                             "DISARM",
                                             "INVUL",
                                             "SNIPE",
                                             "BOMB"]))
    victim = ndb.StringProperty(default="")
    datetime = ndb.DateTimeProperty(required=True)
    place = ndb.StringProperty(default="")
    need_validation = ndb.BooleanProperty(default=True)

