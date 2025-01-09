import json

def load_clients(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

class Settings:
    SECRET_KEY = "dataworkx-secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 300

settings = Settings()
