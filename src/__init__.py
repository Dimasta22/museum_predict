from flask import Flask
from configg import config

app = Flask(__name__)
app.config.from_object(config.Config)
app.debug = True


from src import routes
