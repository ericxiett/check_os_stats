# -*- conding: UTF-8 -*-
import logging

LOG = logging.getLogger('check_openstack_stats')

def init_logging():
    LOG.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_hanlder = logging.FileHandler(
        filename='check_openstack_stats.log',
        mode='a+',
        delay=False
    )
    file_hanlder.setFormatter(formatter)
    LOG.addHandler(file_hanlder)
