"""
Setup:
1. activate python environment
(if creating a virtual environment)
    a. virtualenv env
    b. source env/bin/activate
    c. donwload relevant packages to create a project specific developing environment
2. $ python main.py static/sample-output.json
3. cmd+click the local host address.
4. (optional) Hit shift+command+r (chrome) if css not loading new changes!(cache problem for chrome)
"""
from flask import Flask, render_template, request, redirect, url_for
#from flask_sqlalchemy import SQLAlchemy
import sys
from utils import *

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.db'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     content = db.Column(db.String(200), nullable = False)

filename = sys.argv[-1]

app = Flask(__name__, template_folder='template')

@app.route('/', methods=['GET', 'POST'])
def index():

    json_data, history, item_inter, cooc, simi = read_all(filename, timestamp=0)
    if request.method == 'POST':
        # do stuff when the form is submitted
        return redirect(url_for('update'))

    return render_template('/stage1.html', history= history,
                                          item_inter = item_inter,
                                          cooc = cooc,
                                          simi = simi)


@app.route('/update', methods= ['GET', 'POST'])
def update():
    if request.method == 'POST':
        return redirect(url_for('index'))
    json_data, history, item_inter, cooc, simi = read_all(filename, timestamp=0)

    updated_hist, matrix_update, updated_item, updated_cooc, updated_simi = update_all(json_data, history, item_inter, cooc, simi, 1)
    return render_template('/stage1_update.html', history= updated_hist,
                                          item_inter = updated_item,
                                          cooc = updated_cooc,
                                          simi = updated_simi,
                                          matrix_update= matrix_update)
if __name__ == "__main__":
    app.run(debug = True)
