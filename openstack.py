"""
Management of openstack
"""

import os

from invoke import Collection, task, ctask, run, exceptions
from invoke.exceptions import Failure

Failure

root = lambda p: os.path.abspath(os.path.dirname(__file__) + '/../' + p)
ROOT = root('')
OPENSTACK_DIRS = [
    'ceilometer',
    'cinder',
    'django_openstack_auth',
    'glance',
    'glance_store',
    'heat',
    'heat-cfntools',
    'heat-templates',
    'horizon',
    'keystone',
    'keystonemiddleware',
    'neutron',
    'noVNC',
    'nova',
    'python-neutronclient',
    'python-novaclient',
    'requirements',
    'tempest'
]


@task
def refresh():
    # refresh openstack
    for d in OPENSTACK_DIRS:
        print 'Update of {}'.format(d)
        do = lambda c: run('cd {} && {}'.format(root(d), c))
        run('sudo chown -R kendriu:staff {}'.format(root(d)))
        do('git reset --hard')
        do('git branch --set-upstream-to=origin/master master')
        do('git pull')

    # refresh devstack-vagrant
    d = 'devstack-vagrant'
    do = lambda c: run('cd {} && {}'.format(root(d), c))
    print 'Update of '.format(d)
    run('sudo chown -R kendriu:staff {}'.format(root(d)))
    stash = do('git stash')
    do('git branch --set-upstream-to=origin/master master')
    do('git pull')

    if 'Saved working directory' in stash.stdout:
        do('git stash pop')

    # refresh vagrant
    do('vagrant up manager --provision')

@task
def exists():
    for d in OPENSTACK_DIRS:
        print d + ': ' + str(os.path.exists(root(d)))


namespace = Collection(refresh, exists)