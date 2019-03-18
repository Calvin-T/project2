import socket
import sys

TSedu_DNS_Table = {}

lines = [line.rstrip('\r\n') for line in open("PROJ2-DNSTSedu.txt")]
for line in lines:
	lineSplit = line.split()
	TSedu_DNS_Table[lineSplit[0].lower()] = line

if len(sys.argv) == 2:
	try:
		tsComListenPort = int(sys.argv[1])
	except ValueError:
		exit(1)
else:
	#incorrect arguments
	exit(1)

try:
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("[S]: Server socket created")
except socket.error as err:
	print('socket open error: {}\n'.format(err))
	exit()

#set up the server socket
server_binding = ('', tsComListenPort)
serverSocket.bind(server_binding)
serverSocket.listen(1)
host = socket.gethostname()
print("[S]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[S]: Server IP address is {}".format(localhost_ip))
csockid, addr = serverSocket.accept()
print("[S]: Got a connection request from a client at {}".format(addr))

while True:
	data_from_client = csockid.recv(200)
	recv_msg = data_from_client.decode('utf-8')
	print("[C]: "+ recv_msg)

	if recv_msg == "done":
		break
	else:
		if recv_msg.lower() in TSedu_DNS_Table:
			send_msg =TSedu_DNS_Table[recv_msg.lower()]
			print("[S]: "+ send_msg)
			csockid.send(send_msg.encode('utf-8'))
		else:
			send_msg = recv_msg + " - Error:HOST NOT FOUND"
			print("[S]: " + send_msg)
			csockid.send(send_msg.encode('utf-8'))



# Close the server socket
serverSocket.close()
exit()