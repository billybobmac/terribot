import requests
import json


def setup():
    """ Registers the catfacts plugin. """
    return {'regex': "(catfax)|(cat.?facts)", 'act_on_event': 'message', 'cooldown': 30}


def run(msg):
    """ Returns a random catfact from the catfacts API. """
    result = json.loads((requests.get(url='http://catfacts-api.appspot.com/api/facts')).content.decode("utf-8"))["facts"][0]
    return ({'action': 'send_msg', 'payload': result},)
