#!/usr/bin/python3
"""A script that distributes and archive to my web servers."""
from fabric.api import run, env, put
import os

env.hosts = ['54.87.251.103', '54.236.52.59']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Deploy archive to web server."""
    path = archive_path.split('/')[-1]
    line = path.split('.')[0]
    if not os.path.isfile(archive_path):
        return False
    if put(archive_path, '/tmp/{}'.format(path)).failed:
        return False
    if run('sudo rm -rf /data/web_static/releases/{}'.format(line)).failed:
        return False
    if run('sudo mkdir -p /data/web_static/releases/{}/'.format(line)).failed:
        return False
    if run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
           .format(path, line)).failed:
        return False
    if run('sudo rm /tmp/{}'.format(path)).failed:
        return False
    if run('sudo mv /data/web_static/releases/{}/web_static/* '
           '/data/web_static/releases/{}/'.format(line, line)).failed:
        return False
    if run('sudo rm -rf /data/web_static/releases/{}/web_static'
           .format(line)).failed:
        return False
    if run('sudo rm -rf /data/web_static/current').failed:
        return False
    if run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'
           .format(line)).failed:
        return False
    run('sudo systemctl restart nginx')
    return True
