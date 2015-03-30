# vim: fdm=indent
'''
author:     Fabio Zanini
date:       30/03/15
content:    Main config file for the hivwholeweb web application.
'''
def find_tmp_folder():
    import os

    # Try standard webserver location first
    fn = '/home/hivwholewebu1/tmp/'
    if os.path.isdir(fn):
        return fn

    # Try OS standard
    fn = '/tmp/'
    if os.path.isdir(fn):
        return fn


DEBUG = False
CSRF_ENABLED = True
SECRET_KEY = 'a gig is a gig is a gig'

DATA_SUBFOLDER = 'data'
BLUEPRINTS = {}

TIMEOUT_TMP = '1d'
TMP_ROOT_FOLDER = find_tmp_folder()
