from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import json
import sys

filename = sys.argv[-1]

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.db'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     content = db.Column(db.String(200), nullable = False)
def read_json(filename):
    json_data = [json.loads(line) for line in open(filename, 'r')]
    return json_data
def read_history(filename):
    json_data  =read_json(filename)
    before_matrix = [x for x in json_data if x['time'] == 0]
    interactions = [x for x in before_matrix if x['data'] == 'interactions']
    all_users = np.unique([x['user'] for x in interactions]).tolist()
    all_items = np.unique([x['item'] for x in interactions]).tolist()
    history = []
    for user in all_users:
        curr_hist = [x['item'] for x in interactions if x['user'] == user]
        curr_user = [1 if i in curr_hist else 0 for i in range(len(all_items))]
        history.append(curr_user)
    return history

    
app = Flask(__name__)

@app.route('/')
def index():
    info = read_history(filename)
    return render_template('stage1.html', history= info)

if __name__ == "__main__":
    app.run(debug = True)
