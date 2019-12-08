"""
This python-kafka demo serves as a BACKUP solution

set_up_kafka(): set up kafka and cargo envrionments,  returns a producer 
where we can directly talk to use the push_command function.

The result from the kafka is written to a file `amnesia_result.json` that is automatically generated
in the same directory as the kafka setup directory


Before running, 
1. change the kafka_path to the directory where there is a setup file with kafka folder inside(mine is amnesia-demo)
2. make sure all bash scripts are executable by command: chmod 755 call_* (within bash_scripts folder)

Next step:
1. Integrate reading and updating matrices onto web using buttons
"""
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import subprocess
import shlex
import signal
import json
import appscript
import time
import os
from flaskr.utils import *

KAFKA_HOSTS = ['localhost:9092']
KAFKA_VERSION = (0, 10)
# kafka_path = '/Users/Hengyu/Desktop/Git/deml-project-1'
kafka_path = os.getcwd()

# def set_up_kafka(kafka_path):
#     CURR_CWD = os.getcwd()
#     appscript.app('Terminal').do_script(CURR_CWD+ "/bash_scripts/call_zookeeper.sh "+kafka_path)  
#     time.sleep(5)
#     appscript.app('Terminal').do_script(CURR_CWD+ "/bash_scripts/call_kafka.sh "+kafka_path) 
#     time.sleep(10)
#     appscript.app('Terminal').do_script(CURR_CWD+ "/bash_scripts/call_cargo.sh "+kafka_path) 
#     time.sleep(5)
#     appscript.app('Terminal').do_script(CURR_CWD+ "/bash_scripts/call_consumer.sh "+kafka_path)

#     producer = KafkaProducer(bootstrap_servers=KAFKA_HOSTS, api_version = KAFKA_VERSION)

#     return producer


# def push_command(producer, action, action_list):
#     if action not in ['Add', 'Remove']:
#         print('Enter valid action: Add or Remove')
#         return
#     temp_dict= {"change": action, "interactions": action_list}
#     temp_input = json.dumps(temp_dict, separators=(',', ':'))
#     producer.send('interactions', bytes(temp_input, encoding = 'utf8'))
#     producer.flush()
#     return 

# Below showcases the process of adding and getting results from kafka-python
producer = set_up_kafka(kafka_path)
#%%
init_list = [[0,0], [0,1], [0,2], [0,4], [1,1], [1,2], [2, 0], [2,1], [2,3], [3,1], [3,3]]
push_command(producer, 'Add', init_list)
#%%
RESULT_FILE = os.getcwd() + '/amnesia_result.json'
_, history, item_inter, cooc, simi, all_users, all_items = read_init(RESULT_FILE)
#%%
action_list = [[1,1], [1,2]]
push_command(producer, 'Remove', action_list)
#%%
updated_hist, matrix_update, updated_item, updated_cooc, updated_simi, all_users, all_items = update_all_dynamic(RESULT_FILE, history, item_inter, cooc, simi, all_users, all_items)

#%%
action_list = [[4,1], [4,2]]
push_command(producer, 'Add', action_list)
#%%
updated_hist, matrix_update, updated_item, updated_cooc, updated_simi, all_users, all_items = update_all_dynamic(RESULT_FILE, updated_hist, updated_item, updated_cooc, updated_simi, all_users, all_items)

#%%
action_list = [[3,1], [3,3]]
push_command(producer, 'Remove', action_list)
#%%
updated_hist, matrix_update, updated_item, updated_cooc, updated_simi, all_users, all_items = update_all_dynamic(RESULT_FILE, updated_hist, updated_item, updated_cooc, updated_simi, all_users, all_items)

#%%

##
#TODO: click a button update button, read in new matrix, update and print with animation

# #%%
# # Process
# temp_dict = {"change":"Add", "interactions":[[1,1], [1,2], [2,0], [2,1], [2,3], [3,1], [3,3]]}
# temp_input = json.dumps(temp_dict, separators=(',', ':'))
# producer.send('interactions', bytes(temp_input, encoding='utf8'))
# #%%
# temp_dict = {"change":"Remove", "interactions":[[1,1], [1,2]]}
# temp_input = json.dumps(temp_dict, separators=(',', ':'))
# producer.send('interactions', bytes(temp_input, encoding='utf8'))
# producer.flush()
# #%%

# temp_dict = {"change":"Add", "interactions":[[4,1], [4,2]]}
# temp_input = json.dumps(temp_dict, separators=(',', ':'))
# producer.send('interactions', bytes(temp_input, encoding='utf8'))
# producer.flush()

# #%%

# temp_dict = {"change":"Remove", "interactions":[[3,1], [3,3]]}
# temp_input = json.dumps(temp_dict, separators=(',', ':'))
# producer.send('interactions', bytes(temp_input, encoding='utf8'))
# producer.flush()
# #%%
# appscript.app('Terminal').do_script("Desktop/Git/amnesia-demo/call_zookeeper.sh")  
# time.sleep(5)
# appscript.app('Terminal').do_script("Desktop/Git/amnesia-demo/call_kafka.sh") 
# time.sleep(10)
# appscript.app('Terminal').do_script("Desktop/Git/amnesia-demo/call_cargo.sh") 
# time.sleep(5)
# appscript.app('Terminal').do_script("Desktop/Git/amnesia-demo/call_consumer.sh") 
# #%%

# #%%
