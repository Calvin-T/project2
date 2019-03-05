import socket
import sys

TScom_DNS_Table = {}

lines = [line.rstrip('\r\n') for line in open("PROJ2-DNSTSedu.txt")]
for line in lines:
	lineSplit = line.split()
	TScom_DNS_Table[lineSplit[0]] = [lineSplit[1], lineSplit[2]]

if len(sys.argv) == 2:
	try:
		tsComListenPort = int(sys.argv[1])
	except ValueError:
		exit(1)
else:
	#incorrect arguments
	exit(1)