"""
Setup:
1. activate python environment
(optional if creating a virtual environment)
    a. virtualenv env
    b. source env/bin/activate
    c. pip install -r requirement.txt (for universal dev/exe envrionment)
2. $ python main_animate.py static/sample-output.json
3. cmd+click the local host address.
4. (optional) Hit shift+command+r (chrome) if css not loading new changes!(cache problem for chrome)
"""
from flask import Flask, render_template
from utils import *
import sys

app = Flask(__name__, template_folder='template')
filename = sys.argv[-1]

@app.route('/')
def home():
    image_folder = os.listdir(os.path.join('static', 'images'))
    image_filenames = [os.path.join('images', file) for file in image_folder if file[-3:] == 'jpg']

    json_data, history, item_inter, cooc, simi,all_users, all_items = read_all(filename, 0)
    
    updated_hist, matrix_update, updated_item, updated_cooc, updated_simi, all_users, all_items = update_all(json_data, history, item_inter, cooc, simi, 1, all_users, all_items)

    # row_diff, hist_diff, item_diff, cooc_diff, simi_diff = read_diff(json_data,history,1)
    desired = matrix_update.index(0)+1 # considering the header here (temp implementations)

    #print(desired)
    num_items = len(history[0])
    num_users = len(history)

    # TODO given we are trying to only use one file, can we just input the changes
    return render_template('/stage1_animate.html', num_users = num_users, 
                                                  num_items = num_items,
                                                  history = history,
                                                  desired = desired,
                                                  item_inter = item_inter, 
                                                  cooc = cooc, 
                                                  simi = simi, 
                                                  updated_hist = updated_hist, 
                                                  updated_item = updated_item, 
                                                  updated_cooc = updated_cooc, 
                                                  updated_simi = updated_simi,
                                                  image_names = image_filenames)


if __name__ == '__main__':
    app.run(debug=False)