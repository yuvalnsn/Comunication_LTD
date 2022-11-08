import re 
from configparser import ConfigParser
def dosomething():
   pass
CONFIG_FILE = "config.ini"

config = ConfigParser()
config.read(CONFIG_FILE)
forbidden_passwords = config["register"]["commonpasswords"].split(",")
password_pattern = config["register"]["passwordpattern"]
min_password_length = config["register"]["minPasswordLength"]

