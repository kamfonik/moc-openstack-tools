import argparse
import ConfigParser
from addusers import Openstack
from config import set_config_file
from keystoneclient.v3 import client
from keystoneauth1.identity import v3
from keystoneauth1 import session
from subprocess import Popen, PIPE

def mailman_update(email_list, mailman_config, action='subscribe'):
    "Subscribe or unsubscribe a list of users to/from a Mailman mailing list"

    subscriber_list = "\n".join(email_list)

    command=mailman_config['{}_command'.format(action)]

    ssh_command = ("ssh -l {mailman_user} {mailman_server} "
                   "{command}").format(command=command, **mailman_config)

    subp = Popen(ssh_command.split(), stdin=PIPE, stderr=PIPE)
    subp.communicate(input=subscriber_list)[0]



if __name__ == "__main__":

    help_description = ("Remove users from OpenStack and the mailing list")
    parser = argparse.ArgumentParser(description=help_description)
    parser.add_argument('-c', '--config',
                        help='Specify configuration file.')
    parser.add_argument('-u', '--user', action="append", required=True,
                        help='Username of the OpenStack account to remove.')
    args = parser.parse_args()

    CONFIG_FILE = set_config_file(args.config)

    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE)

    admin_user = config.get('auth', 'admin_user')
    admin_pwd = config.get('auth', 'admin_pwd')
    admin_project = config.get('auth', 'admin_project')
    auth_url = config.get('auth', 'auth_url')

    setpass_url = config.get('setpass', 'setpass_url')
    auth = v3.Password(auth_url=auth_url,
                       username=admin_user,
                       user_domain_id='default',
                       password=admin_pwd,
                       project_domain_id='default',
                       project_name=admin_project)
    session = session.Session(auth=auth)
    
    ks = client.Client(session=session)

    unsubscribe_emails = []

    for user in args.user:
        ks_user = ks.users.find(name=user)
        unsubscribe_emails.append(ks_user.email)
        ks.users.delete(ks_user)

    mailman_config = dict(config.items('mailman'))
    mailman_update(unsubscribe_emails, mailman_config, action='unsubscribe')
