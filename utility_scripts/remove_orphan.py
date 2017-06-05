#   Copyright 2017 Massachusetts Open Cloud
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
"""Delete a user if they have no

Optionally you can specify that the user account must also be disabled.

Usage:
    python remove_orphan.py [--disabled] <username>
"""
import argparse
import ConfigParser
from keystoneclient.v3 import client
from neutronclient.v2_0 import client as nclient
from keystoneauth1 import session
from keystoneauth1.identity import v3

# This is a hack for now until directory structure is sorted
# When this is removed remember to un-ignore E402 in flake8
import os
import sys
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(THIS_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR)
from config import set_config_file

def get_user_roles(ks_user, ):
    role_list = [ra for ra in ks.role_assignments.list()
                if ra.user['id'] == ks_user.id]
    user_roles = []
    for role_assignment in role_list:
        project = ks.projects.get(role_assignment.scope['project']['id'])
        role = ks.roles.get(role_assignment.role['id'])
        user_roles.append((role.name, project.name))
    return user_roles

parser = argparse.ArgumentParser(
    description=("List all roles of the specified user in any project, or "
                 "all users of the specified project and their roles."))
parser.add_argument('-c', '--config',
                    help='Specify configuration file.')

parser.add_argument('user', help='User to remove if orphaned')
parser.add_argument('--disabled', action='store_true',
                    help='Only delete if user account is disabled')
args = parser.parse_args()

CONFIG_FILE = set_config_file(args.config)

config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)

admin_user = config.get('auth', 'admin_user')
admin_pwd = config.get('auth', 'admin_pwd')
admin_project = config.get('auth', 'admin_project')
auth_url = config.get('auth', 'auth_url')
nova_version = config.get('nova', 'version')

auth = v3.Password(auth_url=auth_url,
                   username=admin_user,
                   user_domain_id='default',
                   password=admin_pwd,
                   project_domain_id='default',
                   project_name=admin_project)
sess = session.Session(auth=auth)

ks = client.Client(session=sess)

try:
    ks_user = (u for u in ks.users.list() if args.user == u.name).next()
except:
    print "User {} not found in Keystone".format(args.user)
    exit()

role_assignments = get_user_roles(ks_user)

if not role_assignments:
    print "User {} has no roles".format(ks_user.name)
    if args.disabled and ks_user.enabled:
        print "User {} is still enabled; skip delete".format(ks_user.name)
    else:
        ks_user.delete()
        print "User {} deleted".format(ks_user.name)
          
else:
    print "Role assignments for user {}".format(ks_user.name)
    for ra in role_assignments:
        print '{:<20}{}'.format(ra[0], ra[1])



