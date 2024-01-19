#!/usr/bin/python3
"""Creates and distributes an archive to
my web servers using the function do_deploy.
"""
from datetime import datetime
from fabric.api import run, put, env, local
import os

env.hosts = ['54.237.93.197', '54.145.238.213']
env.user = "ubuntu"


def deploy():
    """Creates and distributes an archive to servers"""
    path = do_pack()
    if path is None:
        return False

    return do_deploy(path)


def do_pack():
    """Creates a .tgz archive."""
    time = datetime.now().strftime('%Y%m%d%H%M%S')
    path = "versions/web_static_{}.tgz".format(time)
    local("mkdir -p versions")

    if local("tar -cvzf {} web_static".format(path)).succeeded:
        return path
    return None


def do_deploy(archive_path):
    """
    deploys archive to web server
    """
    path = archive_path.split('/')[-1]
    line = path.split('.')[0]
    if not os.path.isfile(archive_path):
        return False
    if put(archive_path, "/tmp/{}".format(path)).failed:
        return False
    if run("sudo rm -rf /data/web_static/releases/{}"
            .format(line)).failed:
        return False
    if run("sudo mkdir -p /data/web_static/releases/{}/"
            .format(line)).failed:
        return False
    if run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(path, line)).failed:
        return False
    if run("sudo rm /tmp/{}".format(path)).failed:
        return False
    if run("sudo mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(line, line)).failed:
        return False
    if run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(line)).failed:
        return False
    if run("sudo rm -rf /data/web_static/current").failed:
        return False
    if run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(line)).failed:
        return False

    return True
