import os, time

# def get_mac(ip):
# 	'''
# 		Accepts an IP address and returns the corresponding MAC address.
# 		If not found in the ARP table, raises ValueError
# 	'''
# 	# ping IP to ensure it's presence in the ARP table
# 	os.system('ping {0} -c 2'.format(ip))

# 	time.sleep(5)

# 	from python_arptable import ARPTABLE

# 	print ARPTABLE

# 	for device in ARPTABLE:
# 		if device['IP address'] == ip:
# 			return device['HW address']

# 	raise ValueError('IP not in ARP table')

from subprocess import Popen, PIPE
import re

def get_mac(ip):
	# ping IP to ensure it's presence in the ARP table
	# os.system('ping {0} -c 2'.format(ip))

	pid = Popen(["arp", "-n", ip], stdout=PIPE)
	s = pid.communicate()[0]
	mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]

	return mac

	raise ValueError('IP not in ARP table')