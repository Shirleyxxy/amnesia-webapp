import numpy as np 
import pandas as pd
import json
from fractions import Fraction
import copy

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
    return history
    
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


def read_update(json_data):
    return [x for x in json_data if x['change'] == -1]

def read_update_result(json_data):
    return [x for x in json_data if x['change'] == 1]

def history_update(history_matrix, json_data, timestamp=1):
    """
    This method makes a deep copy hence the original history_matrix will not be changed
    """
    updated_hist = copy.deepcopy(history_matrix)
    changes = read_update(read_action(read_time(json_data, timestamp), 'interactions'))
    for change in changes:
        updated_hist[change['user']][change['item']] += change['change']
    
    matrix_update = [0 if all(i==0 for i in x ) else 1 for x in updated_hist]
    return updated_hist, matrix_update

def item_inter_update(item_inter, json_data, timestamp=1):
    changes = read_update_result(read_action(read_time(json_data, timestamp), 'item_interactions_n'))
    for change in changes:
        item_inter[change['item']] = change['count']
    return item_inter

def cooc_update(cooc, json_data, timestamp=1):
    changes = read_update_result(read_action(read_time(json_data, timestamp), 'cooccurrences_c'))
    for change in changes:
        cooc[change['item_a']][change['item_b']] = change['num_cooccurrences']
        cooc[change['item_b']][change['item_a']] = change['num_cooccurrences']
    return cooc

def simi_update(simi, json_data, timestamp=1):
    changes = read_update_result(read_action(read_time(json_data, timestamp), 'similarities_s'))
    for change in changes:
        simi[change['item_a']][change['item_b']] = str(Fraction(change['similarity']).limit_denominator())
        simi[change['item_b']][change['item_a']] = str(Fraction(change['similarity']).limit_denominator())
    return simi

def read_all(filename, timestamp=0):
    json_data = read_json(filename)
    history = read_history(json_data, timestamp)
    item_inter = read_item_iteraction(json_data, timestamp)
    cooc = read_cooccurences(json_data, timestamp)
    simi = read_similarity_matrix(json_data, timestamp)
    return json_data, history, item_inter, cooc, simi

def update_all(json_data,history_matrix, item_inter, cooc, simi,  timestamp=1):
    updated_hist, matrix_update = history_update(history_matrix, json_data, timestamp)
    updated_item = item_inter_update(item_inter, json_data, timestamp)
    updated_cooc = cooc_update(cooc, json_data, timestamp)
    updated_simi = simi_update(simi, json_data, timestamp)

    return updated_hist, matrix_update, updated_item, updated_cooc, updated_simi
