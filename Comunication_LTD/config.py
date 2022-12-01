from configparser import ConfigParser

CONFIG_FILE = "config.ini"
config = ConfigParser()
config.read(CONFIG_FILE)

min_password_length = int(config["register"]["minPasswordLength"])
password_pattern = config["register"]["passwordpattern"]
forbidden_passwords = config["register"]["commonpasswords"].split(",")
limit_password_history = int(config["register"]["limitpasswordhistory"])
# login_attempts = config["register"]["log

db_pass=str(config['db_pass']['db_pass'])
emailKey=str(config['emailKey']['key'])

