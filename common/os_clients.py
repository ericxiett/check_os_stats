import os

from keystoneauth1 import loading, session
from novaclient import client


def get_nova_client():
    if os.environ.get('OS_USERNAME') == 'admin':
        print('Can not execute this check with user admin!')
        return
    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(auth_url=os.environ.get('OS_AUTH_URL'),
                                    username=os.environ.get('OS_USERNAME'),
                                    password=os.environ.get('OS_PASSWORD'),
                                    project_name=os.environ.get('OS_PROJECT_NAME'),
                                    user_domain_name=os.environ.get('OS_USER_DOMAIN_NAME'),
                                    project_domain_name=os.environ.get('OS_PROJECT_DOMAIN_NAME'))
    sess = session.Session(auth=auth)
    return client.Client('2.1', session=sess)
