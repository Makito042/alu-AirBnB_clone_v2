#!/usr/bin/python3
"""Deploy web static to different servers"""
import re
from fabric import Connection
from os.path import join, exists, splitext

env_hosts = ["54.89.197.58", "34.229.11.29"]
user = "ubuntu"
key_filename = '~/.ssh/id_rsa'

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def do_deploy(archive_path):
    """
    Deploy a compressed archive to a remote server.
    Args:
        archive_path (str): The path to the compressed archive.
    Returns:
        bool: True if the deployment is successful, False otherwise.
    """

    if not exists(archive_path):
        return False

    for host in env_hosts:
        try:
            conn = Connection(
                host=host, user=user, connect_kwargs={"key_filename": key_filename}
            )
            conn.put(archive_path, "/tmp/")
            file_name = re.search(r'[^/]+$', archive_path).group(0)
            deploy_path = join("/data/web_static/releases/",
                               splitext(file_name)[0])
            conn.sudo("mkdir -p {}".format(deploy_path))

            conn.sudo("tar -xzf /tmp/{} -C {}".format(file_name, deploy_path))

            with conn.cd(deploy_path):
                conn.sudo("mv hbnb_static/* .")  # Update to hbnb_static
                conn.sudo("rm -rf hbnb_static")   # Update to hbnb_static

            conn.sudo("rm /tmp/{}".format(file_name))
            conn.sudo("rm -rf /data/hbnb_static/current")

            conn.sudo('ln -sf {} /data/hbnb_static/current'.format(deploy_path))

        except Exception as err:
            print(f"Deployment failed on {host}: {err}")
            return False

    return True
