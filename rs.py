import socket
import sys

RS_DNS_Table = {}
com_hostname = ""
edu_hostname = ""


lines = [line.rstrip('\r\n') for line in open("PROJ2-DNSRS.txt")]
for line in lines:
	lineSplit = line.split()
	if lineSplit[2] == "NS":
		domainSplit = lineSplit[0].split(".")
		if domainSplit[1] == 'edu':
			edu_hostname = lineSplit[0]
		if domainSplit[1] == 'com':
			com_hostname = lineSplit[0]
	else:
		RS_DNS_Table[lineSplit[0]] = [lineSplit[1], lineSplit[2]]


if len(sys.argv) == 4:
	try:
		rsListenPort = int(sys.argv[1])
		tsEduListenPort = int(sys.argv[2])
		tsComListenPort = int(sys.argv[3])
	except ValueError:
		exit(1)
else:
	#incorrect arguments
	exit(1)
