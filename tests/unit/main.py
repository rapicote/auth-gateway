import os
from auth_gateway.config import Config
from auth_gateway.database import Database
from auth_gateway.gateway import Gateway

def main():
    config = Config(os.environ.get('CONFIG_FILE'))

    database = Database(config.database_url)
    database.create_tables()

    gateway = Gateway(config.gateway_url)
    gateway.start()

if __name__ == '__main__':
    main()