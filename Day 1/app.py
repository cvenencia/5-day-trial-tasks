from flask import Flask
from flask_sock import Sock

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sock = Sock(app)

import routes.index
import routes.scraper
