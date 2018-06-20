import configparser

config = configparser.ConfigParser()
config.read("config.cfg")

name = config['general']['server_name']
port = int(config['server']['port'])
