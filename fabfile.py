from fabric.api import env, sudo, local \
        put, cd


def prod():
    env.user = 'ubuntu'
    env.hosts = ['eyebrowse.csail.mit.edu']
    env.key_filename = '~/.ssh/id_rsa.pub'
    env.server_path = '/eyebrowse-server'
    env.python_path = '/eyebrowse-virtualenv/bin'
    env.graceful = True
    return


def deploy():
    sudo('rm -rf %s/*' % env.server_path)
    local('zip -r code.zip * -x "*.pyc" "*.git"')
    put('code.zip', '%s/' % env.server_path, use_sudo=True)
    sudo('cd %s; unzip -o code.zip' % env.server_path)
    sudo('cd %s; rm -f code.zip' % env.server_path)
    local('rm -f code.zip')

    install_reqs()
    install_cron()

    deploy_static()
    compress_static()


def deploy_static():
    with cd(env.server_path):
        sudo('%s/python manage.py collectstatic -v0 --noinput --clear' %
             (env.python_path))


def compress_static():
    with cd(env.server_path):
        sudo('%s/python manage.py compress --force' % (env.python_path))


def install_reqs():
    sudo('%s/pip install -r %s/requirements.txt' %
         (env.python_path, env.server_path))


def install_cron():
    with cd(env.server_path):
        sudo('%s/python manage.py installtasks' % (env.python_path))


def restart_apache():
    if env.graceful:
        sudo('/usr/sbin/apache2ctl -k graceful')
    else:
        sudo('service apache2 restart')
