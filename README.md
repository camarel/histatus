# histatus
Huawei Hilink status page

## Description

histatus is a simple web page that displays the status of the Huawei Hilink modem. 
It is intended to work on an Open WRT router and makes the WAN connection. 

If you are on the road you can use this tool on a cell phone to clearly see if you have a good 3G / LTE connection.


## Installation

The files from the www directory go directly into the /www folder on the OpenWRT router.

Make the CGI script executable:
```
chmod +x /www/cgi-bin/histatus.py
```

## Usage

To access the status page, simply go to your routers IP address, followed by /vpnstatus.html.

Example:
http://192.168.1.1/signal.html
