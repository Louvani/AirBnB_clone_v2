#!/usr/bin/python3
'''module to compres files of web static'''

import os
from datetime import datetime

from fabric.api import local


def do_pack():
    '''generates a .tgz archive from the contents of the web_static folder'''
    # get datetime
    date = datetime.now().replace(second=0, microsecond=0)
    date = '{}{}{}{}{}'.format(
        date.year, date.month, date.day, date.hour, date.minute)

    # create the folder 'versions' if it doesn't exists
    if not os.path.exists('./versions/'):
        os.mkdir('versions')

    # create the file name
    file = './versions/web_static_{}.tgz'.format(date)

    # compressing files
    to_tgz = local('tar -cvzf {} web_static'.format(file))
    if to_tgz.failed:
        return None
    else:
        return "{}".format(file)
