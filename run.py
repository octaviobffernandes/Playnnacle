import os
from instance.init import create_app

"""
Created this docstring to test dummy commit.
"""
config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
