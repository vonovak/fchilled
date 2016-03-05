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

from flask import Flask, jsonify, request, redirect, url_for
from inspect import getmembers
from flask import render_template
from models.products import db
from pprint import pprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b1cb15a23fa673:f243e376@us-cdbr-iron-east-03.cleardb.net/ad_6797d9adb814dd1'
db.init_app(app)

from models.products import Product

with app.app_context():
    db.create_all() # In case user table doesn't exists already. Else remove it.

@app.route('/')
def Welcome():
    products = Product.query.all()
    #str = pprint.pformat(products.name)
    #return str
    return render_template('index.html', products=products)

@app.route('/setup')
def Setup():
    product1 = Product('Coca-Cola', 1)
    db.session.add(product1)

    product2 = Product('Juice', 1)
    db.session.add(product2)

    product3 = Product('Beer', 1)
    db.session.add(product3)

    db.session.commit()
    return 'setup'

@app.route('/api/picture2', methods=['POST'])
def GetPicture():
    message = {
        'form': request.form,
        'data': request.data,
        'args': request.args,
    }
    pprint(getmembers(request))
    return jsonify(results=message)


@app.route('/api/upload-photo', methods=['POST'])
def upload_file():
    if not os.path.isdir(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
    myFile = request.files['file']
    myFile.save(os.path.join(app.config['UPLOAD_FOLDER'], myFile.filename))
    message = {
        'status': 'uploaded',
    }
    return jsonify(results=message)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port), debug=True)
