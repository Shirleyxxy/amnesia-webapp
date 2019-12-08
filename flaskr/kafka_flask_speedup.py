"""
Before running, change the kafka_path to be the path of the directory where insisde,
there is a setup directory with kafka folder(as the one in amnesia-demo). Or change the bash
scripts for proper setup.

This file requrires manually start zoo, kafka and cargo, then run python kafka_falsk_speedup.py

Include interface

Has not designed pictures and name dictionary.

Not fault proof

Add shoud be column separated: '1,2,3'
"""
from flask import Flask, render_template, redirect, url_for, request, session
from utils import *
import os
import time
from subprocess import PIPE, Popen
from threading  import Thread
from queue import Queue, Empty
import json
import shlex
import sys
from kafka import KafkaProducer
import operator

KAFKA_PATH = os.getcwd()
KAFKA_HOSTS = ['localhost:9092']
KAFKA_VERSION = (0, 10)


# Set up kafka environment

producer = KafkaProducer(bootstrap_servers=KAFKA_HOSTS, api_version = KAFKA_VERSION)


# Set up consumer thread for reading
ON_POSIX = 'posix' in sys.builtin_module_names
CONSUMER_COMMANDS = KAFKA_PATH + '/setup/kafka_2.12-2.3.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic changes'
CONSUMER_COMMANDS = shlex.split(CONSUMER_COMMANDS)

p = Popen(CONSUMER_COMMANDS, stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
q = Queue()
t = Thread(target=enqueue_output, args=(p.stdout, q))
t.daemon = True # thread dies with the program
t.start()

##%%
#Initialization
time.sleep(5)
init_list = [[0,0], [0,1], [0,2], [0,4], [1,1], [1,2], [2, 0], [2,1], [2,3], [3,1], [3,3]]
push_command(producer, 'Add', init_list)


app = Flask(__name__, template_folder = 'template')
app.secret_key = b'a_project'# necessary key for session

@app.route('/')
def index():
    # Read in from kafka consumer msg
    curr_list = [json.loads(x.decode(encoding = 'utf8').strip()) for x in list(q.queue)]
    q.queue.clear()

    history, item_inter, cooc, simi, all_users, all_items = read_init(curr_list)
    name_dict = {'Homer': 0, 'Marge':1, 'Bart':2, 'Lisa':3}

    # Store for continuous update

    session['before_hist'] = history
    session['before_item'] = item_inter
    session['before_cooc'] = cooc
    session['before_simi'] = simi
    
    session['history'] = history
    session['item_inter'] = item_inter
    session['cooc'] = cooc
    session['simi'] = simi
    session['all_users'] = all_users
    session['all_items'] = all_items
    session['matrix_update'] = []
    session['name_dict'] = name_dict
    timestamp = 0
    return redirect(url_for('step_update', timestamp = timestamp))

@app.route('/step_update/<timestamp>', methods = ['GET', 'POST'])
def step_update(timestamp):
    if request.method == 'POST':
        if 'delete_button' in request.form:
            name_dict = session['name_dict']
   
            to_be_delete_user_name = request.form['delete_button'].split()[-1]
            to_be_delete_user = int(name_dict[to_be_delete_user_name])

            timestamp = int(timestamp)+1
            action_list = convert_to_query_delete(to_be_delete_user, session['history'], session['all_users'])
            push_command(producer, 'Remove', action_list)
            time.sleep(1.2)
            updates = [json.loads(x.decode(encoding = 'utf8').strip()) for x in list(q.queue)]
            q.queue.clear()
            before_hist, updated_hist, matrix_update, updated_item, updated_cooc, updated_simi, all_users, all_items = update_all_latest(updates, 
                                                                                                                    session['history'],
                                                                                                                    session['item_inter'], 
                                                                                                                    session['cooc'], 
                                                                                                                    session['simi'], 
                                                                                                                    session['all_users'], 
                                                                                                                    session['all_items'])
            # Update the session variable 
            session['before_hist'] = before_hist
            session['history'] = updated_hist
            
            session['before_item'] = session['item_inter']
            session['item_inter'] = updated_item

            session['before_cooc'] = session['cooc']
            session['cooc'] = updated_cooc

            session['before_simi'] = session['simi']
            session['simi'] = updated_simi

            session['all_users'] = all_users
            session['all_items'] = all_items   
            session['matrix_update'] = matrix_update
            
            return redirect(url_for('step_update', timestamp = timestamp))

        elif 'submit_button' in request.form:
            if request.form['submit_button'] == 'Print Hello World':
                return 'Hello World'


            elif request.form['submit_button'] == 'Add':
                timestamp = int(timestamp)+1
                msg = request.form['add_text']
                new_name = request.form['add_name']
                action_list = convert_to_query_add(msg, session['all_users'], session['all_items'])
                push_command(producer, 'Add', action_list)
                time.sleep(1.2)
                updates = [json.loads(x.decode(encoding = 'utf8').strip()) for x in list(q.queue)]
                q.queue.clear()
                before_hist, updated_hist, matrix_update, updated_item, updated_cooc, updated_simi, all_users, all_items = update_all_latest(updates, 
                                                                                                                        session['history'],
                                                                                                                        session['item_inter'], 
                                                                                                                        session['cooc'], 
                                                                                                                        session['simi'], 
                                                                                                                        session['all_users'], 
                                                                                                                        session['all_items'])
                # Only when adding will update name_dict
                session['name_dict'][new_name] = max(all_users) + 1
                # Update the session variable 
                session['before_hist'] = before_hist
                session['history'] = updated_hist

                session['before_item'] = session['item_inter']
                session['item_inter'] = updated_item

                session['before_cooc'] = session['cooc']
                session['cooc'] = updated_cooc

                session['before_simi'] = session['simi']
                session['simi'] = updated_simi

                session['all_users'] = all_users
                session['all_items'] = all_items   
                session['matrix_update'] = matrix_update

                return redirect(url_for('step_update', timestamp = timestamp))
                 

    timestamp = int(timestamp)
    name_list = [t[0] for t in sorted(session['name_dict'].items(), key = operator.itemgetter(1))]


    return render_template('/step_update.html',
                            before_hist = session['before_hist'],
                            before_item = session['before_item'],
                            before_cooc = session['before_cooc'],
                            before_simi = session['before_simi'],
                            history = session['history'], 
                            item_inter = session['item_inter'],
                            cooc = session['cooc'],
                            simi = session['simi'],
                            matrix_update = session['matrix_update'],
                            timestamp = timestamp,
                            name_list = name_list,
                            num_users = len(session['all_users']), 
                            num_items = len(session['all_items']))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

