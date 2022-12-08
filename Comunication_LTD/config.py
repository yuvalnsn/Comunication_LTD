from configparser import ConfigParser

CONFIG_FILE = "config.ini"
config = ConfigParser()
config.read(CONFIG_FILE)

min_password_length = int(config["register"]["minPasswordLength"])
password_pattern = config["register"]["passwordpattern"]
forbidden_passwords = config["register"]["commonpasswords"].split(",")
limit_password_history = int(config["register"]["limitpasswordhistory"])
loging_attempts = int(config['login']['loginAttempts'])
cooloff_time = int(config['login']['cooloffTime'])
db_pass = config['dbPass']['db_pass']
emailKey = config['emailKey']['key']

