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

    #return ('Hello World23')
# @app.route('/displaygraph')
# def displaygraph():
#     return render_template('chart.html')


@app.route('/allplayersdata',methods=['GET'])
def totaldata():
    client =MongoClient("mongodb+srv://JaisonJose:Password@cluster0.ood9a.mongodb.net/player_stats?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client.get_database('player_stats_db')
    records=db.players_collection
    X=[]
    Y1=[]
    Y2=[]
    Y3=[]
    Y4=[]
    Y5=[]
    Y6=[]
    list=[]
    for item in db.players_collection.find():
        list.append({'Name' : item['player_name'], 'Goal' : int(item['goals'])})

    # for item in db.players_collection.find().limit(10):
    #     X.append(item['player_name'])
    #     Y1.append(item['goals'])
    #     Y2.append(item['shots'])
    #     Y3.append(item['assists'])
    #     Y4.append(item['key_passes'])
    #     Y5.append(item['yellow_cards'])
    #     Y6.append(item['red_cards'])
    data_to_plot=db.players_collection.find()
    string_data=str(data_to_plot)
    print(string_data,file=sys.stderr)
    #return render_template('chart.html',data=data_to_plot)
    return jsonify(list) 

@app.route('/data')
def data():
    client =MongoClient("mongodb+srv://JaisonJose:Password@cluster0.ood9a.mongodb.net/player_stats?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client.get_database('player_stats_db')
    records=db.players_collection
    X=[]
    Y1=[]
    Y2=[]
    Y3=[]
    Y4=[]
    Y5=[]
    Y6=[]
    list=[]
    for item in db.players_collection.find().limit(10):
        list.append({'Name' : item['player_name'], 'Goal' : int(item['goals'])})

    # for item in db.players_collection.find().limit(10):
    #     X.append(item['player_name'])
    #     Y1.append(item['goals'])
    #     Y2.append(item['shots'])
    #     Y3.append(item['assists'])
    #     Y4.append(item['key_passes'])
    #     Y5.append(item['yellow_cards'])
    #     Y6.append(item['red_cards'])
    # data_to_plot=db.players_collection.find().limit(10)
    # string_data=str(data_to_plot)
    # print(string_data,file=sys.stderr)
    #return render_template('chart.html',data=data_to_plot)
    return jsonify(list)   

@app.route('/chart')
def column_chart():
    client =MongoClient("mongodb+srv://JaisonJose:Password@cluster0.ood9a.mongodb.net/player_stats?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client.get_database('player_stats_db')
    records=db.players_collection
    Y1=[]
    Y2=[]
    Y3=[]
    Y4=[]
    Y5=[]
    Y6=[]
    X = {}
    list=[]
    for item in db.players_collection.find().limit(10):
        list.append(item)
        #myDict[]
        #X['player_name']
        # X.append(item['player_name']['goals'])
        # Y1.append(item['goals'])
        # Y2.append(item['shots'])
        # Y3.append(item['assists'])
        # Y4.append(item['key_passes'])
        # Y5.append(item['yellow_cards'])
        # Y6.append(item['red_cards'])


    data_to_plot=db.players_collection.find().limit(10)
    string_data=str(data_to_plot)
    print(string_data,file=sys.stderr)
    return render_template('charts.html',data=data_to_plot)


    # page_connect = urlopen("https://understat.com/league/EPL")
    # page_html = BeautifulSoup(page_connect, "html.parser")
    # json_raw_string=str(page_html.findAll(name="script")[3])
    # start_index = json_raw_string.index("\\")
    # stop_index = json_raw_string.index("');")
    # json_data=json_raw_string[start_index:stop_index]
    # json_data=json_data.encode("utf8").decode("unicode_escape")
    # data=json.loads(json_data)
    # for record in data:
    #     db.players_collection.insert_one(record)
    client =MongoClient("mongodb+srv://JaisonJose:Password@cluster0.ood9a.mongodb.net/player_stats?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client.get_database('player_stats_db')
    records=db.players_collection
    X=[]
    Y1=[]
    Y2=[]
    Y3=[]
    Y4=[]
    Y5=[]
    Y6=[]
    for item in db.players_collection.find().limit(10):
        X.append(item['player_name'])
        Y1.append(item['goals'])
        Y2.append(item['shots'])
        Y3.append(item['assists'])
        Y4.append(item['key_passes'])
        Y5.append(item['yellow_cards'])
        Y6.append(item['red_cards'])


    data_to_plot=db.players_collection.find().limit(10)
    string_data=str(data_to_plot)
    print(string_data,file=sys.stderr)

    # data={'Currency':'Price','BTC':48763.00,'ETH':4018.77,'BNB':532.46,'BCH':444.22}
    return render_template('chart.html',data=data_to_plot)
    # return (data_to_plot)

@app.route('/allplayersdata',methods=['GET'])
@app.route('/schedule')
def schedulejob():
    client =MongoClient("mongodb+srv://JaisonJose:Password@cluster0.ood9a.mongodb.net/player_stats?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client.get_database('player_stats_db')
    
    records=db.players_collection

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
    
    # data={'Currency':'Price','BTC':48763.00,'ETH':4018.77,'BNB':532.46,'BCH':444.22}
    return ('<h1>Data Entered in DB</h1>')

if __name__=="__main__":
    app.run()