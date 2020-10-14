from config import MOESIF_TOKEN


def identify_user(app, environ):
    return str(app)


moesif_settings = {
    'APPLICATION_ID': MOESIF_TOKEN,
    'CAPTURE_OUTGOING_REQUESTS': True,
    'IDENTIFY_USER': identify_user,
    'DEBUG': False
}
