# Assignment 1
# Michel Maroun 27197241


import urllib
import urllib.request
import argparse
import socket
from urllib.parse import urlparse
from urllib import parse
import sys
	
def http_request(args):
	#return back scheme, netloc, path, parms,query, fragment
	args.url = urlparse(args.url)
	#test
	server = args.url.netloc
	if not args.url.netloc:
		server = "localhost"
						
	#default port number
	port = 80
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

	if args.data:
		data = args.data
	elif args.file:
		file = open(args.file, "r")
		data = file.read()
		file.close()
	server = args.url.netloc
	request = "POST " + args.url.path + " HTTP/1.1\r\n" + "Host :" + server + "\r\n" + "User-Agent : Concordia-HTTP/1.0 \r\n"

	if args.headers:
		for h in range(len(args.headers)):
			request += args.headers[h] + "\r\n"

	request +=  "Content-Length:" + str(len(data)) + "\r\n\r\n" + data + "\r\n"
	print(request)
	return request

def terminal(): 
	print("write")	

def print_terminal(response, args):
	if args.verbose: 
		print(response.split("\n\r")[0])
	if args.command == "get":
		print(response.split("\n\r")[1])

#parser
parser = argparse.ArgumentParser(description='Http parser', add_help=False)
	
# Get/Post
parser.add_argument('command', choices=['get','post'], help="Executes a HTTP GET/POST request and prints the response.")

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