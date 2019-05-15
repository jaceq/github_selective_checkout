#!/usr/bin/python

import getpass
import requests
import json
import os

####
# user            needs to be your github username
# base_list_url   is api folder url you need eg. https://api.github.com/repos/:owner/:repo/contents/:path
# base_dir        you local path where to put it's contents
####

user = 'XXX'
base_list_url = 'XXX'
base_dir = 'XXX'
debug = None
#debug = True

password = getpass.getpass('Please type your git password: ')

def expand_files_dirs(url, dir):
  if debug:
    print 'Starging function for url: ' + url
    print 'Current dir: ' + dir
  list = requests.get(url, auth=(user,password))

  data = list.json()

  for entry in data:
    if entry['type'] == 'file':
      f = open(dir + '/' + entry['name'],'w')
      f_content = requests.get(entry['download_url'], auth=(user,password))
      if debug:
        print 'Processing file: ' + entry['name']
        print 'Fetched config from url: ' + entry['download_url']
      f.write(f_content.content)      
      f.close
    elif entry['type'] == 'dir':
      os.mkdir(dir + '/' + entry['name'])
      expand_files_dirs(entry['url'], dir + '/' + entry['name'])

expand_files_dirs(base_list_url, base_dir)
