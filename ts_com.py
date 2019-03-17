import socket
import sys

TScom_DNS_Table = {}

lines = [line.rstrip('\r\n') for line in open("PROJ2-DNSTScom.txt")]
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

	
try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: Server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()

server_binding = ('', tsComListenPort)
serverSocket.bind(server_binding)
serverSocket.listen(1)

csockid, addr = serverSocket.accept()

while True:
	data_from_rs = csockid.recv(200)
	recv_msg = data_from_rs.decode('utf-8')
	print("[RS]: " + recv_msg)

	if recv_msg == "done":
		break
	else:
		send_msg = "Message from ts_com"
		print("[TScom]: " + send_msg)
		csockid.send(send_msg.encode('utf-8'))
	print("")

serverSocket.close()
exit()