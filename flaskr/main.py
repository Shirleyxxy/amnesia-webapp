"""
Setup:
1. activate python environment
(if creating a virtual environment)
    a. virtualenv env
    b. source env/bin/activate
    c. donwload relevant packages to create a project specific developing environment
2. $ python main.py static/sample-outputs.json
3. cmd+click the local host address.
4. (optional) Hit shift+command+r (chrome) if css not loading new changes!(cache problem for chrome)
"""
from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy
import sys
from utils import *

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.db'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     content = db.Column(db.String(200), nullable = False)

filename = sys.argv[-1]

app = Flask(__name__)

@app.route('/')
def index():
    json_data = read_json(filename)
    history = read_history(json_data, 0)
    item_inter = read_item_iteraction(json_data, 0)
    cooc = read_cooccurences(json_data, 0)
    simi = read_similarity_matrix(json_data, 0)

    return render_template('stage1.html', history= history, 
                                          item_inter = item_inter,
                                          cooc = cooc,
                                          simi = simi)

if __name__ == "__main__":
    app.run(debug = True)
