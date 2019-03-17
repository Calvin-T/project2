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
		if lineSplit[0].endswith("edu"):
			edu_hostname = lineSplit[0]
		if lineSplit[0].endswith("com"):
			com_hostname = lineSplit[0]
	else:
		RS_DNS_Table[lineSplit[0]] = [lineSplit[1], lineSplit[2]]

print("com host: " + com_hostname)
print("edu host: " + edu_hostname)

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

while True:
	data_from_client = csockid.recv(200)
	recv_msg = data_from_client.decode('utf-8')
	
	recv_msg = recv_msg.lower()

	print("[C]: "+ recv_msg)

	if recv_msg == "done":
		try:
			tsEduSocket.send("done")
			tsComSocket.send("done")
		except:
			# no need to open sockets since they wont be open
			pass

		break
	else:
		if recv_msg in RS_DNS_Table:
			values= RS_DNS_Table[recv_msg]
			send_msg = recv_msg + " " + values[0]+ " " + values[1]
			print("[RS]: "+ send_msg)
			csockid.send(send_msg.encode('utf-8'))
		else:
			if recv_msg.endswith("edu"):
				#contact ts_edu
				for attempt in range(2):
					try:
						print("[RS]: " + recv_msg)
						tsEduSocket.send(recv_msg)
						data_from_tsedu = tsEduSocket.recv(200)
						msg_received = data_from_tsedu.decode('utf-8')
						print("[TSedu]: " + msg_received)
						csockid.send(data_from_tsedu)
						break;
					except:
						#open socket
						try:
							tsEduSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						except socket.error as err:
							print('socket open error: {} \n'.format(err))
							exit()

						tsEduServer_addr = socket.gethostbyname("localhost") #switch to edu_hostname
						tsEduServer_binding = (tsEduServer_addr, tsEduListenPort)
						tsEduSocket.connect(tsEduServer_binding)

			elif recv_msg.endswith("com"):
				#contact ts_com
				for attempt in range(2):
					try:
						print("[RS]: " + recv_msg)
						tsComSocket.send(recv_msg)
						data_from_tscom = tsComSocket.recv(200)
						msg_received = data_from_tscom.decode('utf-8')
						print("[TScom]: " + msg_received)
						csockid.send(data_from_tscom)
						break;
					except:
						#open socket
						try:
							tsComSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						except socket.error as err:
							print('socket open error: {} \n'.format(err))
							exit()

						tsComServer_addr = socket.gethostbyname("localhost") #switch to com_hostname
						tsComServer_binding = (tsComServer_addr, tsComListenPort)
						tsComSocket.connect(tsComServer_binding)
			else:
				send_msg = recv_msg + " - Error:HOST NOT FOUND"
				print("[RS]: " + send_msg)
				csockid.send(send_msg.encode('utf-8'))
	print("")

serverSocket.close()
exit()




