import numpy as np 
import json
from fractions import Fraction
import copy
import os
import appscript
import time
from kafka import KafkaProducer, KafkaConsumer


KAFKA_HOSTS = ['localhost:9092']
KAFKA_VERSION = (0, 10)

def read_json(filename):
    json_data = [json.loads(line) for line in open(filename, 'r')]
    return json_data

def read_time(json_data, timestamp):
    return [x for x in json_data if x['time'] == timestamp]

def read_action(data_list, action):
    return [x for x in data_list if x['data'] == action]

def read_history(json_data, timestamp):
    """
    This function reads history from json data output in list of lists
    Output[List[List]]:
        size: n_users, each user is a n_item long list
    """
    history_records = read_action(read_time(json_data, timestamp), 'interactions')

    # Get all users and all items, SORTED.
    all_users = sorted(np.unique([x['user'] for x in history_records]).tolist())
    all_items = sorted(np.unique([x['item'] for x in history_records]).tolist())

    history = []
    for curr_user in all_users:
        interactions = [x['item'] for x in history_records if x['user'] == curr_user]
        curr_hist= [1 if item in interactions else 0 for item in all_items]
        history.append(curr_hist)
    return history, all_users, all_items
    
def read_item_iteraction(json_data, timestamp):
    """
    This function outputs the item interaction matrix:
    How many times the items are interacted in total. 
    Output: [List]
        size: number of items
    """
    item_inter = read_time(json_data, timestamp)
    # Item user SORTED
    item_inter = sorted(read_action(item_inter, 'item_interactions_n'), key = lambda x: x['item'])
    return [x['count'] for x in item_inter]

def read_cooccurences(json_data, timestamp):
    """
    This function outputs the co-occurrences matrix:
    Output: [List[List]]:
        size: num_item x num_item: diagonals initialized to '-'
    """
    c = read_action(read_time(json_data, timestamp), 'cooccurrences_c')
    # Matrix is symmetric, hence reading upper half
    item_num = max([x['item_a'] for x in c])+1
    # Create list of lists with list[i][i] initialized to '-'
    cooc = [[0]*i + ['-'] + [0]*(item_num-i-1) for i in range(item_num)]
    for record in c:
        cooc[record['item_a']][record['item_b']] = record['num_cooccurrences']
        cooc[record['item_b']][record['item_a']] = record['num_cooccurrences']
    return cooc

def read_similarity_matrix(json_data,timestamp):
    """
    Similar to read_cooccurences, but output similarity matrix
    
    """
    s = read_action(read_time(json_data, timestamp), 'similarities_s')
    item_num = max([x['item_a'] for x in s])+1
    simi = [[0]*i + ['-'] + [0]*(item_num-i-1) for i in range(item_num)]
    for record in s:
        simi[record['item_a']][record['item_b']] = str(Fraction(record['similarity']).limit_denominator())
        simi[record['item_b']][record['item_a']] = str(Fraction(record['similarity']).limit_denominator())
    return simi


def read_delete(json_data):
    return [x for x in json_data if x['change'] == -1]

def read_add(json_data):
    return [x for x in json_data if x['change'] == 1]

def history_update(history_matrix, json_data, timestamp, all_users, all_items):
    """
    This method makes a deep copy hence the original history_matrix will not be changed
    """
    updated_hist = copy.deepcopy(history_matrix)
    deletion = read_delete(read_action(read_time(json_data, timestamp), 'interactions'))
    addition = read_add(read_action(read_time(json_data, timestamp), 'interactions'))

    if deletion: #if there is deletion
        for change in deletion:
            updated_hist[change['user']][change['item']] += change['change']

    if addition: #if there is addition, always append at the end
        all_users.append(addition[0]['user'])
        added_items = sorted([x['item'] for x in addition])
        updated_hist.append([1 if x in added_items else 0 for x in all_items])

    matrix_update = [0 if all(i==0 for i in x ) else 1 for x in updated_hist]

    return updated_hist, matrix_update, all_users, all_items

def item_inter_update(item_inter, json_data, timestamp=1):
    updated_inter = copy.deepcopy(item_inter)
    changes = read_add(read_action(read_time(json_data, timestamp), 'item_interactions_n'))
    for change in changes:
        updated_inter[change['item']] = change['count']
    return updated_inter

def cooc_update(cooc, json_data, timestamp=1):
    updated_cooc = copy.deepcopy(cooc)
    changes = read_add(read_action(read_time(json_data, timestamp), 'cooccurrences_c'))
    for change in changes:
        updated_cooc[change['item_a']][change['item_b']] = change['num_cooccurrences']
        updated_cooc[change['item_b']][change['item_a']] = change['num_cooccurrences']
    return updated_cooc

def simi_update(simi, json_data, timestamp=1):
    updated_simi = copy.deepcopy(simi)
    changes = read_add(read_action(read_time(json_data, timestamp), 'similarities_s'))
    for change in changes:
        updated_simi[change['item_a']][change['item_b']] = str(Fraction(change['similarity']).limit_denominator())
        updated_simi[change['item_b']][change['item_a']] = str(Fraction(change['similarity']).limit_denominator())
    return updated_simi

def read_all(filename, timestamp=0):
    json_data = read_json(filename)
    history, all_users, all_items = read_history(json_data, timestamp)
    item_inter = read_item_iteraction(json_data, timestamp)
    cooc = read_cooccurences(json_data, timestamp)
    simi = read_similarity_matrix(json_data, timestamp)
    return json_data, history, item_inter, cooc, simi, all_users, all_items

def read_init(filename):
    json_data = read_json(filename)
    history, all_users, all_items = read_history(json_data, 0)
    item_inter = read_item_iteraction(json_data, 0)
    cooc = read_cooccurences(json_data, 0)
    simi = read_similarity_matrix(json_data, 0)
    return json_data, history, item_inter, cooc, simi, all_users, all_items 

def update_all(json_data,history_matrix, item_inter, cooc, simi,  timestamp, all_users, all_items):
    """
    This function is used when specific timestamp is requirement.
    Not applicable anymore but kept for future reference if needed
    """
    updated_hist, matrix_update, all_users, all_items = history_update(history_matrix, json_data, timestamp, all_users, all_items)
    updated_item = item_inter_update(item_inter, json_data, timestamp)
    updated_cooc = cooc_update(cooc, json_data, timestamp)
    updated_simi = simi_update(simi, json_data, timestamp)

    return updated_hist, matrix_update, updated_item, updated_cooc, updated_simi, all_users, all_items


def update_all_dynamic(filename,history_matrix, item_inter, cooc, simi, all_users, all_items):
    """
    Dynamically extracts the latest update given a json file, requiring the previous matrices
    must be the most updated result of the previous timestamp
    """
    json_data = read_json(filename)
    latest_time = json_data[-1]['time']
    updated_hist, matrix_update, all_users, all_items = history_update(history_matrix, json_data, latest_time, all_users, all_items)
    updated_item = item_inter_update(item_inter, json_data, latest_time)
    updated_cooc = cooc_update(cooc, json_data, latest_time)
    updated_simi = simi_update(simi, json_data, latest_time)

    return updated_hist, matrix_update, updated_item, updated_cooc, updated_simi, all_users, all_items


"""
The following functions read in the differences between before and after matrices. 
Not used right now but kept for future use if needed.
"""
def hist_change(json_data, timestamp=1):
    """
    Output in a dict of changed users
    Key is the user, the value is a list of tuples (item, changed_value)
    TODO: Change now only -1, may need more general case
    """
    changes = read_delete(read_action(read_time(json_data, timestamp), 'interactions'))
    users = set([x['user'] for x in changes])

    result = {}
    
    for user in users:
        result[user] = [(x['item'], x['change']) for x in changes if x['user'] == user]

    return result

def item_change(json_data, timestamp):
    """
    Assume change is only once
    """
    changed_result = read_add(read_action(read_time(json_data, timestamp), 'item_interactions_n'))
    result = {x['item']:x['count'] for x in changed_result}
    return result

def cooc_change(json_data, timestamp):
    """
    Output a dict with key as item_a, value as item_b and change_to_value
    """
    changed_result = read_add(read_action(read_time(json_data, timestamp), 'cooccurrences_c'))
    item_as = set(x['item_a'] for x in changed_result)
    result = {}
    for a in item_as:
        result[a] = [(x['item_b'], x['num_cooccurrences']) for x in changed_result if x['item_a'] == a]
    return result

def simi_change(json_data, timestamp=1):
    changed_result = read_add(read_action(read_time(json_data, timestamp), 'similarities_s'))
    item_as = set(x['item_a'] for x in changed_result)
    result = {}
    for a in item_as:
        result[a] = [(x['item_b'], 
                     str(Fraction(x['similarity']).limit_denominator())) for x in changed_result if x['item_a'] == a]
    return result

def read_diff(json_data , history_matrix, timestamp, all_users, all_items):
    """
    Will only delete one user at a time
    """
    # hist update records which row will be deleted
    _, row_update, all_users, all_items = history_update(history_matrix, json_data, timestamp, all_users, all_items)
  
    # desired  = hist_update.index(0)+1

    # Only hist record changed values
    hist_diff = hist_change(json_data, timestamp)
    # Only itet change value is not list
    item_diff = item_change(json_data, timestamp)
    # cooc and simi need to do additional transpose
    cooc_diff = cooc_change(json_data, timestamp)
    simi_diff = simi_change(json_data, timestamp)
    return row_update, hist_diff, item_diff, cooc_diff, simi_diff

def set_up_kafka(kafka_path):
    CURR_CWD = '/'.join(os.getcwd().split('/')[:-1])
    print(CURR_CWD)
    appscript.app('Terminal').do_script(CURR_CWD+ "/bash_scripts/call_zookeeper.sh "+kafka_path)  
    time.sleep(5)
    appscript.app('Terminal').do_script(CURR_CWD+ "/bash_scripts/call_kafka.sh "+ kafka_path) 
    time.sleep(10)
    appscript.app('Terminal').do_script(CURR_CWD+ "/bash_scripts/call_cargo.sh "+ kafka_path) 
    time.sleep(5)
    appscript.app('Terminal').do_script(CURR_CWD+ "/bash_scripts/call_consumer.sh " + kafka_path)

    producer = KafkaProducer(bootstrap_servers=KAFKA_HOSTS, api_version = KAFKA_VERSION)

    return producer

def push_command(producer, action, action_list):
    if action not in ['Add', 'Remove']:
        print('Enter valid action: Add or Remove')
        return
    temp_dict= {"change": action, "interactions": action_list}
    temp_input = json.dumps(temp_dict, separators=(',', ':'))
    producer.send('interactions', bytes(temp_input, encoding = 'utf8'))
    producer.flush()
    return 