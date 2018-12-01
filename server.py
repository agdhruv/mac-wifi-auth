from flask import Flask, request, render_template, session, jsonify
from pymongo import MongoClient, ReturnDocument
import os
from pprint import pprint

from utils import get_mac
from config import DEVICE_LIMIT

app = Flask(__name__)
app.config['SECRET_KEY'] = "omg such secret much wowowowowow"

client = MongoClient('localhost', 27017)
db = client['mac-wifi-auth']

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods = ['POST'])
def login():
	user_ip = request.remote_addr
	user_platform = request.user_agent.platform

	# ping IP to ensure it's presence in the ARP table
	os.system('ping {0} -c 2'.format(user_ip))

	data = request.get_json()

	username = data['username']
	password = data['password']

	db_user = db.users.find_one({"username": username})

	if not db_user:
		return jsonify(error = "Username not found.")

	db_password = db_user['password']

	if password != db_password:
		error = "Incorrect password."
		return jsonify(error = error)

	session['logged_in'] = True
	session['username'] = username

	user_mac = get_mac(user_ip)

	if len(db_user['devices']) < 2:
		# basically, add this mac
		db.users.find_one_and_update(
			{"username": username},
			{
				"$push": {
					"devices": {
						"mac": user_mac,
						"device": user_platform
					}
				}
			},
			return_document = ReturnDocument.AFTER
		)
		return jsonify(message = "Device registered. You now have internet access on this device.")
	else:
		# get device list
		return jsonify(message = "Maximum device limit reached.", devices = db_user['devices'])

@app.route('/deleteDevice', methods = ['POST'])
def deleteDevice():
	data = request.get_json()

	if not session['logged_in']:
		return jsonify('Session timed out. Login again.')
	
	username = session['username']
	mac = data['mac']

	# NOW DELETE THIS MAC YO

	return jsonify(hi="hi")


if __name__ == '__main__':
	app.run(debug = True, port = 8000, host = '0.0.0.0')