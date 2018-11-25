const express = require('express');
var arp = require('node-arp');
var device = require('express-device');

var app = express();

app.use(device.capture());

const port = 8000;

app.get('/', (req, res) => {
	const local_ip = req.connection.remoteAddress.substring(7);
	const device_type = req.device.type;
	arp.getMAC(local_ip, function(err, mac) {
	    if (!err) {
	        console.log(mac);
	    }
	});
	console.log(local_ip, device_type);
	res.send('Hi');
});


app.listen(port, () => {
	console.log(`Server is up on port ${port}.`);
});


// NO COMMUNICATION BEFORE = NO ENTRY FOR THIS IP IN THIS ARP TABLE. Thus, use Arping.