from configparser import ConfigParser

CONFIG_FILE = "config.ini"
config = ConfigParser()
config.read(CONFIG_FILE)

min_password_length = config["register"]["minPasswordLength"]
password_pattern = config["register"]["passwordpattern"]
forbidden_passwords = config["register"]["commonpasswords"].split(",")
# limit_password_history = config["register"]["limitpasswordhistory"]
# login_attempts = config["register"]["loginattempts"]

