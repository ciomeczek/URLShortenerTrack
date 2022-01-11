import os
from dotenv import load_dotenv
from flask import Flask
from flask_socketio import SocketIO

load_dotenv()

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

socketio = SocketIO(app)

import server.urls
import server.sockets
import server.time
