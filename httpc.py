# Assignment 1
# Michel Maroun 27197241

#Lines to test
# GET REQUEST
# py httpc.py get'http://httpbin.org/get?course=networking&assignment=1'
# GET REQUEST WITH VERBOSE OPTION 
# py httpc.py get -v 'http://httpbin.org/get?course=networking&assignment=1'
#	POST REQUEST WITH DATA
# py httpc.py post -h Content-Type:application/json -d {\"Assignment\":1} "http://httpbin.org/post"
# POST REQUEST READ FROM FILE
# py httpc.py post -h Content-Type:application/json -f "argspost.txt" "http://httpbin.org/post"
#	GET REQUEST WITH OUTPUT TO FILE  
# py httpc.py get "http://httpbin.org/get?course=networking&assignment=1" -o textfile.txt

import argparse
import socket
from urllib.parse import urlparse
import urllib.request
import sys

def http_request(args):
	#return back scheme, netloc, path, parms,query, fragment
	if urlparse(args.url):
		args.url = urlparse(args.url)
	#test
	server = args.url.netloc
	if not args.url.netloc:
		server = "localhost"
						
	#default port number
	port = 80

	#If it is a redirect and a get method 
	if args.command == "get" and isRedirect(args) :
		print("\n\rRedirecting from: " + args.url.scheme + "://" + args.url.netloc + args.url.path.split(" ")[0] + "?" +args.url.query + "\n\r")
		#Returns args url .url = Redirect url
		redirect = getRedirectUrl(args)
		httprequest = map_request(redirect)
		connect(server, httprequest, args)
	elif args.command == "get": 
		url =  args.url.netloc + args.url.path.split(" ")[0]
		#map CMD arguments and request
		httprequest = map_request(args)
		connect(server, httprequest, args)	
	else:
		url = args.url.scheme + "://" + args.url.netloc + args.url.path.split(" ")[0]
		#map CMD arguments and request
		httprequest = map_request(args)
		connect(server, httprequest, args)

def map_request(args):
	if args.command == "get":
		return get(args)
	if args.command == "post":
		return post(args)	

#connection to socket and sending request
def connect(server, httprequest, args):
	port = 80
	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		connection.connect((server, port))
		connection.send(httprequest.encode("utf-8"))
		response = connection.recv(4096).decode("utf-8")
		#print to terminal
		print_terminal(response, args)
		
	finally:
		connection.close()

#get request		
def get(args):
	request = "GET "
	request += args.url.path
	server = args.url.netloc
	if args.url.query: 
		request += "?" + args.url.query
	request += " HTTP/1.1\r\n" + "Host: " + server + "\r\n" + "User-Agent: Concordia-HTTP/1.0 \r\n"	
	#If user adds header to command
	if args.headers: 
		for i in range(len(args.headers)):
			request += args.headers[i] + "\r\n"
	request += "\r\n"
	return request 	

#post request		
def post(args):	
	data = ""
	tempdata = ""
	if args.data:
		data = args.data
	elif args.file:
		file = open(args.file, "r")
		data = file.read()
		file.close()

	server = args.url.netloc
	request = "POST " + args.url.path + " HTTP/1.0\r\n" + "Host :" + server + "\r\n" + "User-Agent : Concordia-HTTP/1.0 \r\n"

	if args.headers:
		for i in range(len(args.headers)):
			request += args.headers[i] + "\r\n"

	request +=  "Content-Length:" + str(len(data)) + "\r\n\r\n" + data + "\r\n"

	return request

def print_terminal(response, args):
	if args.verbose: 
		print(response.split("\n\r")[0])
	if args.command == "get":
		print(response.split("\n\r")[1])
	if args.command == "post":
		print(response.split("\n\r")[1])
	output_file(response, args)

#write to file
def output_file(response, args):
	file = ""
	if args.output:
		try: 
			file = open(args.output, "w+")
			#If print with verbose
			if args.verbose:
				file.write(response)
			else:
				file.write(response.split("\n\r")[1])
		except: 
			print("ERROR OPENING FILE")
		finally: 
			file.close()
# returns true or false depending if url has code 302 (redirect)
def isRedirect(args):
	if args.url:
		url = args.url.scheme + "://" + args.url.netloc + args.url.path.split(" ")[0] + "?" +args.url.query
		request = urllib.request.urlopen(url)
		if request.geturl() != url:
			return True 
		else: 
			return False
	else: 
		return False
# Method to get parsed redirect url
def getRedirectUrl(args):
	url = args.url.scheme + "://" + args.url.netloc + args.url.path.split(" ")[0] + "?" +args.url.query
	request = urllib.request.urlopen(url)
	args.url = urlparse(request.geturl())
	return args
#parser
parser = argparse.ArgumentParser(description='Http parser', add_help=False)
	
# Get/Post
parser.add_argument('command', choices=['get','post', 'help'], help="Executes a HTTP GET/POST request and prints the response.")

#add Data Command 
parser.add_argument('-d', dest="data", action="store", metavar="inline-data", help="Associates an inline data to the body HTTP POST")
#add Verbose Command
parser.add_argument('-v','--verbose', action="store_true")
#add File command 
parser.add_argument('-f', dest='file', action='store', metavar="inline-data", help="Read arguments from text file.")
#add Header command
parser.add_argument('-h', dest='headers', action='append')
# Url
parser.add_argument('url', type=str, action="store", help="Url HTTP request is sent to")
#Output
parser.add_argument('-o', dest="output", action="store")

args = parser.parse_args()
http_request(args)	