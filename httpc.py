import urllib
import urllib.request
import argparse
import socket
from urllib.parse import urlparse
import sys
	
def http_request(args):
	#return back scheme, netloc, path, parms,query, fragment
	args.url = urlparse(args.url)
	#test
	print(args)
	if not args.url.netloc:
		server = "localhost"
						
	#default port number
	port = 80
	url = args.url.scheme + "://" + args.url.netloc + args.url.path.split(" ")[0]
	print(url)
	request = urllib.request.urlopen(url)
	print(request.read())
	print(request.status)
	#map CMD arguments and request
	map_request(args, request)
		
		
def map_request(args, request):
	if args.get:
		get(args, request)
	if args.post:
		post()
	
#get request		
def get(args, request):
	print("get")
	
		
#post request		
def post():	
	print("post")
	
	
#parser
parser = argparse.ArgumentParser(description='Http parser', add_help=False)
	
#add argument for get		
parser.add_argument('-g', '--get', action='store_true')
#add argument for post
parser.add_argument('-p', '--post', action='store_true')
#add Data Command 
parser.add_argument('-d', dest="data", action="store", metavar="inline-data", help="Associates an inline data to the body HTTP POST")
#add Verbose Command
parser.add_argument('-v','--verbose', action="store_true")
#add File command
parser.add_argument('-f', dest='file', action='store_true')
#add Header command
parser.add_argument('-h', dest='headers', action='append')
# Url
parser.add_argument('url', type=str, action="store", help="Url HTTP request is sent to")

	
args = parser.parse_args()
	
	
http_request(args)	