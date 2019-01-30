import urllib
import argparse
import socket
from urllib.parse import urlparse

class HttpRequest:

	
	def http_request(args):
		#return back scheme, netloc, path, parms,query, fragment
		args.url = urlparse(args.url)
		#test
		print(args.url)
		server = args.netloc
	
	#default port number
	port = 80			
	
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