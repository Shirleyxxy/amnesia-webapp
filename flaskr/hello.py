from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy
import numpy as np
import json
import sys

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'