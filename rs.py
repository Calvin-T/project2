import socket
import sys

RS_DNS_Table = {}
com_IP_addr = ""
edu_IP_addr = ""


lines = [line.rstrip('\r\n') for line in open("PROJ2-DNSRS.txt")]
for line in lines:
	lineSplit = line.split()
	if lineSplit[2] == "NS":
		domainSplit = lineSplit[0].split(".")
		if lineSplit[0].endswith(".edu"):
			edu_IP_addr = lineSplit[1]
		if lineSplit[0].endswith(".com"):
			com_IP_addr = lineSplit[1]
	else:
		RS_DNS_Table[lineSplit[0].lower()] = line

print(".com host: " + com_IP_addr)
print(".edu host: " + edu_IP_addr)

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

try:
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("[RS]: Server socket created")
except socket.error as err:
	print('socket open error: {}\n'.format(err))
	exit()

server_binding = ('', rsListenPort)
serverSocket.bind(server_binding)
serverSocket.listen(1)
csockid, addr = serverSocket.accept()
print("[RS]: Got a connection request from a client at {}".format(addr))

#msg = "Connected to RS Server"
#csockid.send(msg.encode('utf-8'))
try:
	tsEduSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
	print('socket open error: {} \n'.format(err))
	exit()

# tsEduServer_addr = socket.gethostbyname("localhost") #switch to edu_hostname
tsEduServer_binding = (edu_IP_addr, tsEduListenPort)
tsEduSocket.connect(tsEduServer_binding)

try:
	tsComSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
	print('socket open error: {} \n'.format(err))
	exit()

# tsComServer_addr = socket.gethostbyname("localhost") #switch to com_hostname
tsComServer_binding = (com_IP_addr, tsComListenPort)
tsComSocket.connect(tsComServer_binding)

while True:
	data_from_client = csockid.recv(200)
	recv_msg = data_from_client.decode('utf-8').lower()

	print("[C]: "+ recv_msg)

	if recv_msg == "done":
		tsEduSocket.send(recv_msg.encode('utf-8'))
		tsComSocket.send(recv_msg.encode('utf-8'))
		break
	else:
		if recv_msg in RS_DNS_Table:
			send_msg = RS_DNS_Table[recv_msg.lower()]
			print("[RS] to [C]: "+ send_msg)
			csockid.send(send_msg.encode('utf-8'))
		else:
			if recv_msg.endswith("edu"):
				print("[RS] to [edu]:  " + recv_msg)
				tsEduSocket.send(recv_msg.encode('utf-8'))
				data_from_tsedu = tsEduSocket.recv(200)
				msg_received = data_from_tsedu.decode('utf-8')
				print("[edu]: " + msg_received)
				csockid.send(msg_received.encode('utf-8'))

			elif recv_msg.endswith("com"):
				print("[RS] to [com]: " + recv_msg)
				tsComSocket.send(recv_msg.encode('utf-8'))
				data_from_tscom = tsComSocket.recv(200)
				msg_received = data_from_tscom.decode('utf-8')
				print("[com]: " + msg_received)
				csockid.send(msg_received.encode('utf-8'))
			else:
				send_msg = recv_msg + " - Error:HOST NOT FOUND"
				print("[RS]: " + send_msg)
				csockid.send(send_msg.encode('utf-8'))
	print("")

serverSocket.close()
exit()




