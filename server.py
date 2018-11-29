from flask import Flask, request, render_template
from utils import get_mac
import os

app = Flask(__name__)

@app.route('/')
def index():
	user_ip = request.remote_addr
	user_platform = request.user_agent.platform

	# ping IP to ensure it's presence in the ARP table
	ping = os.system('ping {0} -c 2'.format(user_ip))

	user_mac = get_mac(user_ip)

	return "Hi"

if __name__ == '__main__':
	app.run(debug = True, port = 8000, host = '0.0.0.0')