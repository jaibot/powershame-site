from fabric.api import *

# the user to use for the remote commands
env.user = 'powershame'
# the servers where the commands are executed
env.hosts = [ 'www.powershame.com' ]

def pack():
    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    # figure out the release name and version
    dist = local('python setup.py --fullname', capture=True).strip()
    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '/tmp/powershame.tar.gz')
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    run('mkdir /tmp/powershame')
    with cd('/tmp/powershame'):
        run('tar xzf /tmp/powershame.tar.gz')
    with cd('/tmp/powershame/%s' % dist ):
        with prefix('source /home/powershame/.virtualenvs/powershame-site/bin/activate'):
            # now setup the package with our virtual environment's
            # python interpreter
            run('python setup.py install')
    # now that all is set up, delete the folder again
    run('rm -rf /tmp/powershame /tmp/powershame.tar.gz')
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    #run('touch /var/www/powershame/powershame.wsgi')

def clean():
    #remove local build files
    local('rm -rf dist Powershame_Server.egg-info build')
    local('pyclean .')
