from flask import Flask, render_template
import numpy as np
import json
import sys
from utils import *

app = Flask(__name__)


@app.route('/')
def render_static():
    return render_template('hello_test.html')

if __name__ == '__main__':
    app.run()