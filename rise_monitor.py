#!/usr/bin/env python
from urllib2 import urlopen
from urllib import urlencode
url = "http://10.42.0.108:3000/readings.json"
block_size = 120 # 1 minute at 0.5s sampling rate

def mean(items):
  return sum(items) / len(items)

def post(intensity, height):
  d = { "reading[height]": height, "reading[intensity]": intensity }
  print "Posting: {}".format(d)
  remote = urlopen(url, urlencode(d))
  res = remote.read()
  print "\tresponse: {}".format(res)

def handle_data(source):
  while True:
    height_values, intensity_values = list(), list()
    for i in range(block_size):
      line = source.readline()
      if line.strip() != "":
        intensity, height = line.split(',')
        try:
          height_values.append(float(height))
          intensity_values.append(int(intensity))
        except ValueError as e: pass # Skip unparseable lines
    post(mean(intensity_values), mean(height_values))

if __name__ == "__main__":
  import sys
  handle_data(sys.stdin)