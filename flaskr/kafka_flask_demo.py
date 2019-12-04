'''
This file contains a demo for using kafka with python for real-time update

Include Cargo file from amnesia-demo. Build the cargo envrionment first.

Did NOT implement the user interaction, hence can only click the update once
for dummy demo purpose(with fixed next step update)

Before running, change the kafka_path to be the path of the directory where insisde,
there is a setup directory with kafka folder(as the one in amnesia-demo). Or change the bash
scripts for proper setup.
'''
from flask import Flask, render_template, redirect, url_for, request, session
from utils import *
import os
import time

kafka_path = '/Users/Hengyu/Desktop/Git/deml-project-1'
RESULT_FILE = kafka_path + '/amnesia_result.json'

# Set up kafka environment
producer = set_up_kafka(kafka_path)
time.sleep(5) # pause for file writing

#Initialization
init_list = [[0,0], [0,1], [0,2], [0,4], [1,1], [1,2], [2, 0], [2,1], [2,3], [3,1], [3,3]]
push_command(producer, 'Add', init_list)
time.sleep(3)

app = Flask(__name__, template_folder = 'template')
app.secret_key = b'a_project'# necessary key for session

@app.route('/')
def index():
    # Read in from kafka consumer msg
    json_data, history, item_inter, cooc, simi, all_users, all_items = read_init(RESULT_FILE)

    # Store for continuous update
    session['json_data'] = json_data
    session['history'] = history
    session['item_inter'] = item_inter
    session['cooc'] = cooc
    session['simi'] = simi
    session['all_users'] = all_users
    session['all_items'] = all_items

    timestamp = 0
    return redirect(url_for('step_update', timestamp = timestamp))

@app.route('/step_update/<timestamp>', methods = ['GET', 'POST'])
def step_update(timestamp):
    if request.method == 'POST':

        timestamp = int(timestamp)+1
        # Dummy demo purpose, TODO: connect with user interface later
        # Here is a fixed update 
        action_list = [[1,1], [1,2]]
        push_command(producer, 'Remove', action_list)
        # Pause for file writing
        time.sleep(3)
        # Extract the latest update from kafka result
        updated_hist, matrix_update, updated_item, updated_cooc, updated_simi, all_users, all_items = update_all_dynamic(RESULT_FILE, 
                                                                                                                        session['history'],
                                                                                                                        session['item_inter'], 
                                                                                                                        session['cooc'], 
                                                                                                                        session['simi'], 
                                                                                                                        session['all_users'], 
                                                                                                                        session['all_items'])
        # Update the session variable 
        session['history'] = updated_hist
        session['item_inter'] = updated_item
        session['cooc'] = updated_cooc
        session['simi'] = updated_simi
        session['all_users'] = all_users
        session['all_items'] = all_items

        return redirect(url_for('step_update', history = session['history'], 
                                timestamp = timestamp, 
                                num_users = len(session['all_users']), 
                                num_items = len(session['all_items']) ))


    timestamp = int(timestamp)

    return render_template('/step_update.html',history = session['history'],timestamp = timestamp,
                           num_users = len(session['all_users']), 
                           num_items = len(session['all_items']))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)