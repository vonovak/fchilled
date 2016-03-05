# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'b1cb15a23fa673'
app.config['MYSQL_DATABASE_PASSWORD'] = 'f243e376'
app.config['MYSQL_DATABASE_DB'] = 'ad_6797d9adb814dd1'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-iron-east-03.cleardb.net'


@app.route('/')
def Welcome():
    return app.send_static_file('index.html')


@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'


@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 21},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)


@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)


@app.route('/api/picture', methods=['POST'])
def GetPicture():
    message = {
        'message': request.form
    }
    return jsonify(results=message)


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
