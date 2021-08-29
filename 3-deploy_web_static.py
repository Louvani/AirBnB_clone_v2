#!/usr/bin/python3
''' Module '''

import os
from datetime import datetime

from fabric.api import env, run, put, local

env.hosts = ['3.89.116.12', '54.89.68.173']
env.user = 'ubuntu'


def do_deploy(archive_path):
    '''distributes an archive to your web servers'''
    if not os.path.exists(archive_path):
        return False

    # Upload the archive to the /tmp/ directory of the web server
    upload = put(archive_path, '/tmp/')
    if upload.failed:
        return False

    # create the folder
    file_ext = archive_path.split('/')[1]
    file = file_ext.split('.')[0]

    folder = run('mkdir -p /data/web_static/releases/{}'.format(file))
    if folder.failed:
        return False

    # Uncompress the archive to the folder
    uncom = run(
        'tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(
            file_ext, file))
    if uncom.failed:
        return False
    # Move files
    mv = run('mv /data/web_static/releases/{}/web_static/* \
        /data/web_static/releases/{}'.format(file, file))
    if mv.failed:
        return False

    # Delete the archive from the /tmp/
    delete = run('rm /tmp/{}'.format(file_ext))
    if delete.failed:
        return False

    # Delete the symbolic link /data/web_static/current from the web server
    rm = run('rm -rf /data/web_static/current')
    if rm.failed:
        return False

    # Create a new the symbolic link /data/web_static/current
    ln = run(
        "ln -s /data/web_static/releases/{} /data/web_static/current".format(
            file))
    if ln.failed:
        return False

    return True


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
    file = 'versions/web_static_{}.tgz'.format(date)

    # compressing files
    to_tgz = local('tar -cvzf {} web_static'.format(file))
    if to_tgz.failed:
        return None
    else:
        return "./{}".format(file)


def deploy():
    '''creates and distributes an archive to your web servers,
    using the function deploy'''
    # Call the do_pack() function and store the path of the created archive
    path = do_pack()
    if path is None:
        return False

    # Call the do_deploy(archive_path) function,
    # using the new path of the new archive
    result = do_deploy(path)
    return result
