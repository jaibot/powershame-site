import os

SECRET_KEY = 'dfddsdsds983iureriueg'
DEBUG = True
FACEBOOK_APP_ID = '649973058365254'
FACEBOOK_APP_SECRET = '49f27560185f42c8c8fe80f3934c7d27'

class Config(object):
    DEBUG = True
    TESTING = False
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
    FBAPI_APP_ID = os.environ.get('FACEBOOK_APP_ID')
    FBAPI_APP_SECRET = os.environ.get('FACEBOOK_SECRET')
    #FBAPI_SCOPE = ['user_likes', 'user_photos', 'user_photo_video_tags']
    FBAPI_SCOPE = []
