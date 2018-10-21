import os
from instance.init import create_app
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / 'vars.env'
load_dotenv(dotenv_path=env_path)

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
