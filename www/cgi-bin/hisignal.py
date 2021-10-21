#!/usr/bin/env python

# Get the connection status from a Huawei HiLink modem
# like E3276 or E3372.
#
# Returns data via JSON to be used in a HTML document.
#
# Based on
# https://github.com/trick77/huawei-hilink-status
# https://github.com/arska/e3372

import requests
import xmltodict
import time
import math
import json

def to_size(size):
  if (size == 0):
    return '0 Bytes'
  size_name = ('Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
  i = int(math.floor(math.log(size,1024)))
  p = math.pow(1024,i)
  s = round(size/p,2)
  return '%s %s' % (s,size_name[i])

def get_connection_status(status):
  result = 'n/a'
  if status == '2' or status == '3' or status == '5' or status == '8' or status == '20' or status == '21' or status == '23' or status == '27' or status == '28' or status == '29' or status == '30' or status == '31' or status == '32' or status == '33':
    result = 'Connection failed, the profile is invalid'
  elif status == '7' or status == '11' or status == '14' or status == '37':
    result = 'Network access not allowed'
  elif status == '12' or status == '13':
    result = 'Connection failed, roaming not allowed'
  elif status == '201':
    result = 'Connection failed, bandwidth exceeded'
  elif status == '900':
    result = 'Connecting'
  elif status == '901':
    result = 'Connected'
  elif status == '902':
    result = 'Disconnected'
  elif status == '903':
    result = 'Disconnecting'
  elif status == '904':
    result = 'Connection failed or disabled'
  return result

def get_roaming_status(status):
  result = 'n/a'
  if status == '0':
    result = 'Disabled'
  elif status == '1':
    result = 'Enabled'
  return result

def get_signal_level(level):
  result = '-'
  if level == '1':
    result = u'\u2581'
  if level == '2':
    result = u'\u2581' + u'\u2583'
  if level == '3':
    result = u'\u2581' + u'\u2583' + u'\u2584'
  if level == '4':
    result = u'\u2581' + u'\u2583' + u'\u2584' + u'\u2586'
  if level == '5':
    result = u'\u2581' + u'\u2583' + u'\u2584' + u'\u2586' + u'\u2588'
  return result

def get_network_type(type):
  result = 'n/a'
  if type == '0':
    result = 'No Service'
  elif type == '1':
    result = 'GSM'
  elif type == '2':
    result = 'GPRS (2.5G)'
  elif type == '3':
    result = 'EDGE (2.75G)'
  elif type == '4':
    result = 'WCDMA (3G)'
  elif type == '5':
    result = 'HSDPA (3G)'
  elif type == '6':
    result = 'HSUPA (3G)'
  elif type == '7':
    result = 'HSPA (3G)'
  elif type == '8':
    result = 'TD-SCDMA (3G)'
  elif type == '9':
    result = 'HSPA+ (4G)'
  elif type == '10':
    result = 'EV-DO rev. 0'
  elif type == '11':
    result = 'EV-DO rev. A'
  elif type == '12':
    result = 'EV-DO rev. B'
  elif type == '13':
    result = '1xRTT'
  elif type == '14':
    result = 'UMB'
  elif type == '15':
    result = '1xEVDV'
  elif type == '16':
    result = '3xRTT'
  elif type == '17':
    result = 'HSPA+ 64QAM'
  elif type == '18':
    result = 'HSPA+ MIMO'
  elif type == '19':
    result = 'LTE (4G)'
  elif type == '41':
    result = 'UMTS (3G)'
  elif type == '44':
    result = 'HSPA (3G)'
  elif type == '45':
    result = 'HSPA+ (3G)'
  elif type == '46':
    result = 'DC-HSPA+ (3G)'
  elif type == '64':
    result = 'HSPA (3G)'
  elif type == '65':
    result = 'HSPA+ (3G)'
  elif type == '101':
    result = 'LTE (4G)'
  return result

class HuaweiE3372(object):
  BASE_URL = 'http://{host}'
  COOKIE_URL = '/html/index.html'
  session = None
  connection_status = 0
  reply = {}

  def __init__(self,host='192.168.8.1'):
    self.host = host
    self.base_url = self.BASE_URL.format(host=host)
    self.session = requests.Session()

    try:
      # get a session cookie by requesting the COOKIE_URL
      r = self.session.get(self.base_url + self.COOKIE_URL, timeout=2)
    except requests.exceptions.RequestException as e:
      self.reply['error'] = 'no modem'
      self.session = None

  def get(self,path):
    return xmltodict.parse(self.session.get(self.base_url + path).text).get('response',None)

  def connection_status(self):
    if self.session is None:
      return

    response = self.get('/api/monitoring/status')
    self.connection_status = response['ConnectionStatus']
    signal_strength = response['SignalStrength']
    signal_level = response['SignalIcon']
  
    self.reply['status'] = get_connection_status(self.connection_status)
    if self.connection_status == '901':
      self.reply['network'] = get_network_type(response['CurrentNetworkType'])
      self.reply['signal'] = signal_level
      self.reply['level'] = get_signal_level(signal_level)
      self.reply['roaming'] = get_roaming_status(response['RoamingStatus'])

  def provider(self):
    if self.session is None:
      return

    if self.connection_status == '901':
      response = self.get('/api/net/current-plmn')
      self.reply['operator'] = response['ShortName']

  def print_json(self):
    json_dump = json.dumps(self.reply)

    print("Content-type:application/json\r\n\r\n")
    print(json_dump)

def main():
  e3372 = HuaweiE3372()
  e3372.connection_status()
  e3372.provider();

  e3372.print_json();

if __name__ == "__main__":
  main()
