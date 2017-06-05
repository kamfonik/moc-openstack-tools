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
import ConfigParser
import os
from keystoneclient.v3 import client
from neutronclient.v2_0 import client as nclient
from keystoneauth1 import session
from keystoneauth1.identity import v3
from keystoneauth1.exceptions.http import NotFound


# Use only one of the auth sections below

"""
# Uncomment this section to authenticate with a config file

CONFIG_FILE = '/path/to/file'
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)

admin_user = config.get('auth', 'admin_user')
admin_pwd = config.get('auth', 'admin_pwd')
admin_project = config.get('auth', 'admin_project')
auth_url = config.get('auth', 'auth_url')
"""


"""
# Uncomment this section to authenticate with an environment set from a
# keystonerc file
admin_user = os.environ.get('OS_USERNAME')
admin_pwd = os.environ.get('OS_PASSWORD')
admin_project = os.environ.get('OS_PROJECT_NAME')
auth_url = os.environ.get('OS_AUTH_URL')
"""

# Uncomment this section to authenticate with hard coded values
admin_user = 'admin'
admin_pwd = 'secret'
admin_project = 'admin'
auth_url = 'http://some-auth-url'


auth = v3.Password(auth_url=auth_url,
                   username=admin_user,
                   user_domain_id='default',
                   password=admin_pwd,
                   project_domain_id='default',
                   project_name=admin_project)
sess = session.Session(auth=auth)

keystone = client.Client(session=sess)

ks_projects = keystone.projects.list()
neutron = nclient.Client(session=sess)

all_quotas = [q for q in neutron.list_quotas()['quotas']]

for qset in all_quotas:
    proj_id = qset['tenant_id']
    try:
        project = keystone.projects.get(proj_id)
        print project
    except NotFound:
        # it seems when projects are deleted their quota sets are not ?
        print "%s not found" % proj_id
