from python_arptable import ARPTABLE

def get_mac(ip):
	'''
		Accepts an IP address and returns the corresponding MAC address.
		If not found in the ARP table, raises ValueError
	'''
	for device in ARPTABLE:
		if device['IP address'] == ip:
			return device['HW address']

	raise ValueError('IP not in ARP table')