import socket
import sys

rsHostname = ""
rsListenPort = 0

if len(sys.argv) == 3:
	rsHostname = sys.argv[1]
	try:
		rsListenPort = int(sys.argv[2])
	except ValueError:
		exit(1)
else:
	#incorrect arguments
	exit(1)