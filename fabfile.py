from fabric.api import *
from fabric.contrib.project import rsync_project

def staging():
    env.hosts = ['eyebrowse-staging.csail.mit.edu']
    env.server_path = '/eyebrowse-server'
    env.python_path = '/eyebrowse-server'
    env.graceful = True
    return

def prod():
    env.hosts = ['eyebrowse.csail.mit.edu']
    env.server_path = '/eyebrowse-server'
    env.python_path = '/eyebrowse-server'
    env.graceful = True
    return
    
def deploy():
    rsync_project(remote_dir=env.server_path, local_dir='.',
                  exclude=["*.pyc", "*.git/", "fabfile.py"], delete=True)
    install_reqs()
    

def install_reqs():
    run('%s/pip install -r %s/requirements.txt' % (env.python_path, env.server_path))
    
def restart_apache():
    if env.graceful:
        sudo("/usr/sbin/apache2ctl -k graceful")
    else:
        sudo("service apache2 restart")
