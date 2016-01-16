'''DEPRECATED'''


from entities import Team, Player
from util.custom_errors import RegistrationError
from google.appengine.ext import ndb
import re

ROLES = set(["sniper", "demo", "medic"])


def register_team(teamname):
    ''' Store in datastore.'''
    teamname_p = re.sub(r'[^a-zA-z\s]', '', teamname)
    team = Team()
    team.key = ndb.Key('Team', teamname_p)
    team.put()
    return teamname_p


def register_player(number, name, role, teamname, secret_code):
    ''' Stores player in datastore '''
    ''' Process name'''
    name_p = re.sub(r'[^a-zA-z]', '', name)

    ''' Process role'''
    role_p = role.strip().lower()
    try:
        role_p in ROLES
    except:
        raise RegistrationError("invalid role")  # Exception handled by caller

    ''' Process teamname'''
    try:
        team_key = ndb.Key('Team', teamname)
        team = team_key.get()
        if role_p == "sniper":
            if team.sniper:
                team.sniper = number
            else:
                raise RegistrationError("role on your team is already taken.")
        elif role_p == "medic":
            if team.medic:
                team.medic = number
            else:
                raise RegistrationError("role on your team is already taken.")
        else:
            if team.demo:
                team.demo = number
            else:
                raise RegistrationError("role on your team is already taken.")
    except:
        raise RegistrationError("invalid teamname")

    ''' Generate secrete code '''
    if len(secret_code) > 4:
        raise RegistrationError("secret code too long")
    else:
        try:
            secret_code_p = int(secret_code)
            secret_code_query = Player.query()
            used_numbers = secret_code_query.fetch(projection=["secret_code"])
            for number in used_numbers:
                if secret_code_p == number:
                    raise RegistrationError("secret code already taken. \
                                            Please try another one.")
        except:
            raise RegistrationError("secret code must be an integer")

    '''Make and save player object in datastore'''
    player = Player(state="alive", role=role_p, secret_code=secret_code_p)
    player.key = ndb.Key('Player', number, paret=ndb.Key('Team', teamname))
    player.put()
    return name_p, role_p, secret_code, teamname


# TOOD: should a player be able to find the status of his teammates?
# TODO: player changes role
