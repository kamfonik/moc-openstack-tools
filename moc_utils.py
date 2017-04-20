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
"""Utility functions shared by multiple modules"""
from os import path
from keystoneauth1.identity import v3
from keystoneauth1 import session


def get_absolute_path(file_path):
    """Convert a possibly relative file path to an absolute file path"""
    if not path.isabs(file_path):
        this_dir = path.dirname(path.abspath(__file__))
        abs_path = path.abspath(path.join(this_dir, file_path))
        return abs_path
    else:
        return file_path


def select_rows(match_value, col_index, all_rows, header=True):
    """Select only rows where the value in the search column matches
 
    This allows the caller to process requests from one user or project at a
    time if needed, for example when processing individual helpdesk tickets.
    inputs:
        match_value    the value to search for
        col_index      the column index to search
        all_rows       a list of rows.  A row is a list of cell values, so
                       all_rows should have the format:
                           [ [head0, head1], [val0, val1], [val2, val3]]
        header         Whether all_rows[0] contains column headers.
                       Default: True
    """
    # Preserve index and mimic the return format of enumerate(rows)
    select_rows = [(all_rows.index(row), row) for row in all_rows
                   if (row != []) and
                      (row[col_index].lower() == match_value.lower())]
    if not select_rows:
        raise ValueError('No match found for `{}`'.format(match_value))
    # put the header row back
    if header:
        select_rows.insert(0, (0, all_rows[0]))
    return select_rows


def get_auth_session(config):
    """Set up a a keystoneauth1 session using credentials from config file"""
    
    admin_user = config.get('auth', 'admin_user')
    admin_pwd = config.get('auth', 'admin_pwd')
    admin_project = config.get('auth', 'admin_project')
    auth_url = config.get('auth', 'auth_url')

    auth = v3.Password(auth_url=auth_url,
                       username=admin_user,
                       user_domain_id='default',
                       password=admin_pwd,
                       project_domain_id='default',
                       project_name=admin_project)
    auth_session = session.Session(auth=auth)

    return auth_session
