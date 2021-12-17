from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from bson import json_util
import json
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from html.parser import HTMLParser
import sys

app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')




@app.route('/allplayersdata',methods=['GET'])
def totaldata():
    client =MongoClient("mongodb+srv://JaisonJose:Password@cluster0.ood9a.mongodb.net/player_stats?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client.get_database('player_stats_db')
    records=db.players_collection

    list=[]
    for item in db.players_collection.find():
        list.append({'Name' : item['player_name'], 'Goal' : int(item['goals'])})


    return jsonify(list) 

@app.route('/data',methods=['GET'])
def data():
    client =MongoClient("mongodb+srv://JaisonJose:Password@cluster0.ood9a.mongodb.net/player_stats?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client.get_database('player_stats_db')
    records=db.players_collection

    list=[]
    for item in db.players_collection.find().limit(10):
        list.append({'Name' : item['player_name'], 'Goal' : int(item['goals'])})

    return jsonify(list)   

@app.route('/chart')
def column_chart():
    client =MongoClient("mongodb+srv://JaisonJose:Password@cluster0.ood9a.mongodb.net/player_stats?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client.get_database('player_stats_db')
    records=db.players_collection
    list=[]
    for item in db.players_collection.find().limit(10):
        list.append(item)
    return render_template('charts.html')


@app.route('/refreshstandings',methods=['GET'])
def schedulejob():
    client =MongoClient("mongodb+srv://JaisonJose:Password@cluster0.ood9a.mongodb.net/player_stats?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client.get_database('player_stats_db')

    page_connect = urlopen("https://understat.com/league/EPL")
    page_html = BeautifulSoup(page_connect, "html.parser")
    json_raw_string=str(page_html.findAll(name="script")[3])
    start_index = json_raw_string.index("\\")
    stop_index = json_raw_string.index("');")
    json_data=json_raw_string[start_index:stop_index]
    json_data=json_data.encode("utf8").decode("unicode_escape")
    data=json.loads(json_data)
    db.players_collection.delete_many({})

    for record in data:
        db.players_collection.insert_one(record)
    
    return ('<h1>Data Entered in DB</h1>')

if __name__=="__main__":
    app.run()