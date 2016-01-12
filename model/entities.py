from google.appengine.ext import ndb


class Player(ndb.Model):
    '''Pklayer object is child of a Team object.
    Key: phone number
    Has:
        state,
        role,
        secret_codei
    Parent: team'''
    state = ndb.StringProperty()
    role = ndb.StringProperty()
    secret_code = ndb.IntegerProperty()


class Team(ndb.Model):
    '''Team object
    Key: team_name
    Has:
        to_kill
        target_of
        sniper
        medic
        demo
    Child: Player'''
    to_kill = ndb.StringProperty(default="")
    target_of = ndb.StringProperty(defualt="")
    sniper = ndb.StringProperty(default="")
    medic = ndb.StringProperty(default="")
    demo = ndb.StringProperty(default="")


class Event(ndb.Model):
    '''Event object
    Key: appengine assigned numeric id
    Has:
        attacker
        action
        victim
        time
        place
        picture TODO(georgeteo): GAE cloud storage implement
    '''
    attacker = ndb.StringProperty()
    action = ndb.StringProperty()
    victim = ndb.StringProperty()
    time = ndb.DateTimeProperty()
    place = ndb.StringProperty()
