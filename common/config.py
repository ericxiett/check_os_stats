from configparser import ConfigParser

CONF_FILE = 'conf'

def get_config(conf_file):
    config = ConfigParser()
    config.read(conf_file)
    return config


CONF = get_config(CONF_FILE)
