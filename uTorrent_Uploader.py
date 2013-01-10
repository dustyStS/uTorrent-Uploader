#!/usr/bin/env python

import re
import requests
import sys
import os

from optparse import OptionParser

TOKEN_URL = "http://192.168.1.200:9090/gui/token.html"
USER = "WEBUI_USERNAME_HERE"
PASS = "WEBUI_PASSWORD_HERE"

def get_token():
	r = requests.get(TOKEN_URL, auth=(USER,PASS))
	data = r.text
	GUID_COOKIE = r.cookies['GUID']
	regex = re.compile(r".*<div\s+id='token'.*>(.*)</div>")
	m = regex.match(data)
	if m != None:
		return (m.group(1), GUID_COOKIE)


def post_torrent(token, GUID_COOKIE, torrent_file, dir):
	POST_URL  = "http://192.168.1.200:9090/gui/?token=%s&action=add-file" % token
	if dir == None:
		files = {'torrent_file': open(torrent_file, 'rb')}
	elif dir:
		full_path = dir + torrent_file
		files = {'torrent_file': open(full_path, 'rb')}

	cookie = dict(GUID=GUID_COOKIE)
	r = requests.post(POST_URL, files=files, cookies=cookie, auth=(USER,PASS))

	if r.status_code == 200:
		print "[*] Upload completed successfully.."
	else:
		print "[*] Upload failed."

def process_filename(token, GUID_COOKIE, filename):
	post_torrent(token, GUID_COOKIE, filename, dir=None)

def process_directory(token, GUID_COOKIE, dir):
	for fname in os.listdir(dir):
		if fname.endswith(".torrent"):
			print "[+] Adding torrent: %s." % fname
			post_torrent(token, GUID_COOKIE, fname, dir)


def main():
	usage = "Usage: %prog [options] arg1"
	parser = OptionParser(usage=usage, version="%prog v1.0")
	parser.add_option("-f", "--file", dest="filename", help="Specify a filename to upload", metavar="FILE")
	parser.add_option("-d", "--directory", dest="directory", help="Specify a directory", metavar="DIRECTORY")	
	(options, args) = parser.parse_args()

	if options.filename == None and options.directory  == None:
		parser.print_help()
		sys.exit(0)

	token, GUID_COOKIE = get_token()

	if options.filename:
		process_filename(token, GUID_COOKIE, options.filename)
	elif options.directory:
		process_directory(token, GUID_COOKIE, options.directory)


main()
