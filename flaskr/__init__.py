'''
__init__.py contains the application factory, and it tells Python that
the flaskr directory should be treated as a package.
'''

import os
import json
from flask import Flask

def create_app(test_config=None):
    '''
    Application factory function.
    '''
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/hello')
    def hello():
        return 'This is a test. Hello World!'

    @app.route('/data')
    def read_data():
        filename = os.path.join(app.static_folder, 'sample-output.json')
        data = [json.loads(line) for line in open(filename, 'r')]
        return data[0]['data']

    return app
