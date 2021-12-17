from flask import Flask, jsonify, request, render_template
from urllib.request import urlopen
from pymongo import MongoClient
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import json
import time

while True:
	
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
	
	print('Data Entered in DB')
	time.sleep(86400)