import numpy as np 
import json
from fractions import Fraction

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




