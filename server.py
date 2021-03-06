from flask import Flask, request, render_template, session, jsonify
from pymongo import MongoClient, ReturnDocument
import os
from pprint import pprint
import socket

from utils import get_mac

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

	try:
		user_mac = get_mac(user_ip)
	except ValueError as e:
		error = "IP not found. Contact IT Department."
		return jsonify(error = error)

	session['this_mac'] = user_mac

	# check if mac alread registered
	for device in db_user['devices']:
		if device['mac'] == user_mac:
			return jsonify(message = "This device is already registered. You now have internet access.")

	if len(db_user['devices']) < db_user['device_limit']:
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
		return jsonify(message = "Maximum device limit reached.", devices = db_user['devices'], this_mac = user_mac)

@app.route('/deleteDevice', methods = ['POST'])
def deleteDevice():
	data = request.get_json()

	if not session['logged_in']:
		return jsonify('Session timed out. Login again.')
	
	username = session['username']
	mac = data['mac']
	user_platform = request.user_agent.platform
	this_mac = session['this_mac']

	try:
		# delete old MAC
		db.users.find_one_and_update(
			{"username": username},
			{	
				"$pull": {
					"devices": {
						"mac": mac
					}
				}
			},
			return_document = ReturnDocument.AFTER
		)

		# add new mac
		db.users.find_one_and_update(
			{"username": username},
			{	
				"$push": {
					"devices": {
						"device": user_platform,
						"mac": this_mac
					}
				}
			},
			return_document = ReturnDocument.AFTER
		)
	except Exception as e:
		print e
		return jsonify(error = "Error in updation. Contact IT.")

	return jsonify(message = "Device registered. You now have internet access.")


if __name__ == '__main__':
	print "##### Running on", socket.gethostbyname(socket.gethostname()), "#####"
	app.run(debug = True, port = 8000, host = '0.0.0.0')





