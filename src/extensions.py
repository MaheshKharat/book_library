from flask import Flask, g, abort, request
from config import Config
from src.db import db

app = Flask(__name__, static_folder='static', template_folder='templates')
