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
"""Script allowing a new user to reset their password securely.

The script performs the following  actions:
    - Resets the user's OpenStack password to a random string
    - Add the user, new password, and PIN to the Setpass service
    - Generates a Setpass link the user will visit to reset their password
    - Send the link via email to the user

Usage:
    python reset-password.py <username> <PIN>

The PIN must be a 4-digit number and the user must provide it to successfully
set their new password.

For more information on the Setpass service see:
https://github.com/CCI-MOC/setpass
"""
import sys
import re
import argparse
import ConfigParser
from keystoneclient.v3 import client

# local import
from message import TemplateMessage
from setpass import SetpassClient, random_password
from config import set_config_file
from moc_utils import get_auth_session


def validate_pin(pin):
    """Check that PIN is 4 digits"""
    if not re.match('^([0-9]){4}$', pin):
        msg = "'{}' is not a valid four-digit PIN".format(pin)
        raise argparse.ArgumentTypeError(msg)
    else:
        return pin


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Reset user's password")
    parser.add_argument('username',
                        help='of the user whose password you wish to reset')
    parser.add_argument('PIN',
                        type=validate_pin,
                        help='Four-digit PIN provided by the user')
    parser.add_argument('-c',
                        '--config',
                        help='Specify configuration file.')

    args = parser.parse_args()
    
    if args.config is not None:
        CONFIG_FILE = set_config_file(args.config)
    else:
        CONFIG_FILE = set_config_file()
    
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE)
    
    setpass_url = config.get('setpass', 'setpass_url')

    sess = get_auth_session(config)

    setpass = SetpassClient(sess, setpass_url)
    keystone = client.Client(session=sess)
    
    user = [usr for usr in keystone.users.list() if usr.name == args.username]
    if not user:
        print "User {} not found".format(args.username)
        sys.exit(1)
    else:
        user = user[0]

    newpass = random_password(16)
    
    keystone.users.update(user, password=newpass)
    token = setpass.get_token(user.id, newpass, args.PIN)
   
    url = setpass.get_url(token)

    email_config = dict(config.items('email_defaults'))
    email_config.update(dict(config.items('reset_password_email')))
    
    email = TemplateMessage(email=args.username, fullname=args.username,
                            setpass_token_url=url, **email_config)

    try:
        email.send()
    except:
        email.dump_to_file(config)
        raise
        
    print "Password successfully reset for user {}".format(user.name)
