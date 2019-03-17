import socket
import sys

rsHostname = ""
rsListenPort = 0

results = []

if len(sys.argv) == 3:
	rsHostname = str(sys.argv[1])
	try:
		rsListenPort = int(sys.argv[2])
	except ValueError:
		exit(1)
else:
	#incorrect arguments
	exit(1)

# socket to talk to rs server
try:
	rsSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#print("[C]: RS Client socket created")
except socket.error as err:
	print('socket open error: {} \n'.format(err))
	exit()

rsServer_addr=socket.gethostbyname(rsHostname)
rsServer_binding=(rsServer_addr,rsListenPort)
rsSocket.connect(rsServer_binding)

#data_from_RSserver = rsSocket.recv(200)
#print("[C]: Data received from  rs server: {}".format(data_from_RSserver.decode('utf-8')))


with open("PROJ2-HNS.txt") as file:
	lines = [line.rstrip('\r\n') for line in file]
	for line in lines:
		print("[C]: "+ line)
		rsSocket.send(line.encode('utf-8'))
		data_from_RSserver = rsSocket.recv(200)
		print("[S]: " + data_from_RSserver)
		print("")
		results.append(data_from_RSserver.decode('utf-8'))


	closing_msg = "done"
	rsSocket.send(closing_msg.encode('utf-8'))

file = open("RESOLVED.txt","w")
for result in results:
	file.write(result + "\n")
file.close()

rsSocket.close()
exit()