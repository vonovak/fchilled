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
from flask import render_template
from models.products import db
import time
import base64
from vision import callvisionapi
from watsonthread import watsonThread
from notification import sendNotification

app = Flask(__name__)
app.config[
    # 'SQLALCHEMY_DATABASE_URI'] = 'mysql://b1cb15a23fa673:f243e376@us-cdbr-iron-east-03.cleardb.net/ad_6797d9adb814dd1'
    'SQLALCHEMY_DATABASE_URI'] = 'db2://user05351:Lf7lc1LEbJls@5.10.125.192:50000/SQLDB'
app.config['UPLOAD_FOLDER'] = './uploads'
db.init_app(app)

from models.products import Product

with app.app_context():
    db.create_all()  # In case user table doesn't exists already. Else remove it.


@app.route('/')
def Welcome():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/setup')
def Setup():
    product1 = Product('cocacola', 'Coca-Cola', 0)
    db.session.add(product1)

    product2 = Product('juice', 'Juice', 0)
    db.session.add(product2)

    product3 = Product('beer', 'Beer', 0)
    db.session.add(product3)

    product4 = Product('waterbottle', 'Bottled Water', 0)
    db.session.add(product4)

    db.session.commit()
    return 'setup'


@app.route('/watsontest')
def watsontest():
    return callvisionapi('test.jpg')

@app.route('/gcmtest')
def gcmtest():
    sendNotification()
    return 'notification sent'


@app.route('/api/upload-photo', methods=['POST'])
def upload_file():
    if not os.path.isdir(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])

    filename = str(int(round(time.time() * 1000)))
    myFile = open(app.config['UPLOAD_FOLDER'] + '/' + filename + '.jpg', 'w')
    myFile.write(base64.b64decode(request.data))
    myFile.close()

    thread1 = watsonThread(filename)
    thread1.start()

    return "File " + filename + " uploaded"


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port), debug=True)
