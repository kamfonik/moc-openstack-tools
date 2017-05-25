#   Copyright 2016 Massachusetts Open Cloud
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


#import datetime
import json
import random # temp import
#import smtplib
#import uuid
#
#from email.mime.text import MIMEText
from flask import Response
from flask import request, render_template, redirect, session
from keystoneauth1.identity import v3
from keystoneauth1 import session as ks_session
from keystoneauth1.exceptions import http as ksa_exceptions
#
#from setpass import config
#from setpass import model
import model
import wsgi
#from setpass import exception
#
application = wsgi.app
#
#CONF = config.CONF

@wsgi.app.route('/test', methods=['GET'])
def view_test():
    return Response(response='TESTING SERVER', status=200)

@wsgi.app.route('/accounts', methods=['GET'])
def view_new_request():
    # FIXME: something like project_list = get_openstack_projects()
    project_list = ['Project 1', 'project 2', 'PROJECT 3']
    return render_template('account_request.html', projects=project_list)


@wsgi.app.route('/accounts', methods=['POST'])
def view_new_user_confirm():
    request_info  = {'first_name': request.form['first_name'],
                     'last_name': request.form['last_name']}
    
    user_exists = request.form['account_exists']
    new_project = request.form['project']

    if user_exists == 'true':
        os_user = request.form['openstack_username']
        os_pass = request.form['openstack_password']
        # KEYSTONE AUTH TO GET USER ID & EMAIL
        request_info['user_id'] = 'keystone_userID'
        request_info['email'] = 'keystone_email'        
    else:
        request_info['email'] = request.form['email']
         
    new_request = model.Request(**request_info)
    model.db.session.add(new_request)

    if user_exists == 'false': 
        new_user_info = {'phone': request.form['phone'],
                         'username': request.form['email'],
                         'organization': request.form['organization'],
                         'org_role': request.form['org_role'],
                         'sponsor': request.form['sponsor'],
                         'pin': request.form['pin'],
                         'comment': request.form['comment']}
        new_user = model.NewUser(new_request, **new_user_info)
        model.db.session.add(new_user)
 
    if new_project == 'true':
        project_info = {'project_name': request.form['project_name'],
                        'description': request.form['project_description']}
  
        new_proj = model.NewProject(new_request, **project_info)
        model.db.session.add(new_proj) 
    else:
        # FIXME: sometihng like new_request.project_id = get_keystone_project_id() 
        new_request.project_id = "keystone_id_existing_project"
 
    model.db.session.commit()
      
    return Response(response='Request ID # {} has been submitted for approval.'.format(new_request.id), status=200)

@wsgi.app.route('/quotas', methods=['GET'])
def view_quota_auth():
    return render_template('quota_auth.html')

@wsgi.app.route('/quotas', methods=['POST'])
def view_new_quotas():
    username = request.form['ks_user']
    password = request.form['ks_password']

    # something like:
    #   ks_user = get_keystone_user(username, password)
    #   project_list = get_user_projects(ks_user)
    #   quota_list = {};
    #   for p in project_list:
    #       quota_list[p] = get_project_quotas(p)
 
    # For now we have dummy data:
    project_list = ["dummy project 1", "dummy project 2", "dummy project 3"] 
    quota_list = {}; 
    for p in project_list:
        quota_list[p] = {};
        quota_list[p]['vcpus'] = random.randint(1,20)
        quota_list[p]['ips'] = random.randint(1,20)
        quota_list[p]['instances'] = random.randint(1,20)
      
    return render_template('quotas.html', projects=project_list, quotas=quota_list)

if __name__ == '__main__':
    wsgi.app.run(port=5001, host='0.0.0.0', debug=True)
