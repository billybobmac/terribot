import tempfile
import requests


def setup():
    """ Registers the up yours plugin. """
    return {'regex': "up yours", 'act_on_event': 'message'}


def run(msg):
    """ Returns the upyours image. """
    image = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    response = requests.get('http://i.imgur.com/am5PDx6.jpg')
    image.write(response.content)
    image.close()
    return ({'action': 'send_photo', 'payload': image.name},)
