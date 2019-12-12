"""
2) Create the following Routes in your Flask Application (Use the data you persisted in Module 9)

Default Route ("/") - Go to a simple html template page that tells about your data.
GET ("/item") - Will return UP TO 1000 items from your data.
GET ("/item/<id>") - Will return a single item from your data, by ID. If you data does not have a unique identifier then please let me know and I will help you get one added.
DELETE("/item/<id>") - Will delete a single item (again, you will need a unique column name)
POST ("/item") - As opposed to GET, POST will create a new item in your database. The body of the request will contain the item to be added.

I am having hard time with the CSS

Questions for Mckelly:
1)Css not working
2)Interactive HTML
3)

I can get a zip file from a URL using a 3rd party library
Use this to work has an API type data?

If you want to get around hitting the api too many times, use a timer
"""

from pymongo import MongoClient
from flask import Flask, g, render_template, abort, request
from bson.json_util import dumps
from bson.objectid import ObjectId
import ssl
import json
import dns
import os
import pprint
import pandas as pd

# Configure the connection
client = MongoClient("mongodb+srv://jaceiverson:vufspUcCvsFX2yCT@test-ol2kq.mongodb.net/test?retryWrites=true",ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
db=client['Test']
champ=db['League Champions']
championFile={}

#puts all the champions into a dictionary locally
for x in champ.find():
    championFile[str([x['id']][0])]=x

# Setup Flask
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/', methods=['GET'])
def hello():
    return render_template('APILanding.html')

@app.route('/api/v1/champions', methods=['GET'])
def allItems():
    allChamps=champ.find()
    return dumps(allChamps), 200

@app.route('/api/v1/championstats', methods=['GET'])
def allStats():
    allChamps = champ.find()
    everyone = dumps(allChamps)
    everyone = json.loads(everyone)
    stats = {}
    for x in range(len(everyone)):
        stats[everyone[x]['name']] = everyone[x]['stats']
    #this probably isn't the best practice, but I did it anyway.
    #pd.DataFrame.from_dict(stats).T.to_html('/Users/jaceiverson/Documents/College/Python Night Class/FinalRiot/Try2/Project/templates/statsTest.html')
    return dumps(stats),200

@app.route('/api/v1/championnames', methods=['GET'])
def allNames():
    return dumps(championFile.keys()), 200

@app.route('/api/v1/champions/<string:id>', methods=['GET'])
def oneItem(id):
    #this works
    book = champ.find_one({"id": str(id)})
    return dumps(book), 200

@app.route('/api/v1/champions/<string:id>/stats', methods=['GET'])
def oneChampStats(id):
    book = champ.find_one({"id": str(id)})
    stats=book['stats']
    return dumps(stats), 200


@app.route('/api/v1/champions/<string:id>/spells', methods=['GET'])
def oneChampSpells(id):
    book = champ.find_one({"id": str(id)})
    stats = book['stats']
    return dumps(stats), 200

@app.route('/api/v1/champions/<string:id>/', methods=['DELETE'])
def removeOneItem():
    pass

@app.route('/api/v1/champions/<string:id>/', methods=['POST'])
def postOneItem():
    pass

if __name__ == '__main__':
    app.run(debug=True)