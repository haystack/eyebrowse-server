from fabric.api import *

def amy():
    env.user = 'axz'

def staging():
    env.hosts = ['eyebrowse-staging.csail.mit.edu']
    env.server_path = '/eyebrowse-server'
    env.python_path = '/eyebrowse-virtualenv/bin'
    env.graceful = True
    return

def prod():
    env.hosts = ['eyebrowse.csail.mit.edu']
    env.server_path = '/eyebrowse-server'
    env.python_path = '/eyebrowse-virtualenv/bin'
    env.graceful = True
    return
    
def deploy():
   
    sudo("rm -rf %s/*" % env.server_path)
    local('zip -r code.zip * -x "*.pyc" "*.git"')
    put("code.zip", "%s/" % env.server_path, use_sudo=True)
    sudo("cd %s; unzip -o code.zip" % env.server_path)
    sudo("cd %s; rm -f code.zip" % env.server_path)
    local("rm -f code.zip")
    
    deploy_static()
    
    install_reqs()
    
def deploy_static():
    with cd(env.server_path):
        sudo('./manage.py collectstatic -v0 --noinput')

def install_reqs():
    sudo('%s/pip install -r %s/requirements.txt' % (env.python_path, env.server_path))
    
def restart_apache():
    if env.graceful:
        sudo("/usr/sbin/apache2ctl -k graceful")
    else:
        sudo("service apache2 restart")
