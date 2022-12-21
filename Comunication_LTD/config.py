from configparser import ConfigParser

CONFIG_FILE = "config.ini"
config = ConfigParser()
config.read(CONFIG_FILE)

min_password_length = int(config['register']["minPasswordLength"])
password_pattern = config['register']["passwordPattern"]
forbidden_passwords = config['register']["commonPasswords"].split(",")
limit_password_history = int(config['register']["limitPasswordHistory"])
loging_attempts = int(config['login']['loginAttempts'])
cooloff_time = int(config['login']['cooloffTime'])
db_pass = config['dataBase']['db_pass']
db_name = config['dataBase']['db_name']
emailKey = config['emailKey']['key']
sec_lvl = config['security']['secLevel']