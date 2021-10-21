# histatus
Huawei Hilink status page

## Description

histatus is a simple web page that displays the status of the Huawei Hilink modem. 
It is intended to work on an Open WRT router where the Hilink modem makes the WAN connection.

Purpose is to display clearly on a cell phone or laptop the current signal strength of your modem. This can help you to find a spot with a better connection.

The status is refreshed every 5 seconds via javascript.
There is a little dot on the left top corner that indicates when new data was fetched from the modem.

![status-4g](https://user-images.githubusercontent.com/47444685/138318500-8a0e2871-df4b-4ebd-9edc-57d47eb03a9b.jpg)

## Installation

The files from the www directory go directly into the /www folder on the OpenWRT router.

Make the CGI script executable:
```
chmod +x /www/cgi-bin/hisignal.py
```

## Usage

To access the status page, simply go to your routers IP address, followed by /signal.html.

Example:
http://192.168.1.1/signal.html
