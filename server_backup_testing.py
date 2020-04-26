  
#!/usr/bin/env python3
"""
	server.py = TCP chat App server that listens all the clients' requests on port 8888.
	It helps the sender send messages to the receiver.
	Then it returns a "success" to sender. Then it prints the message that was sent.
	Author: Zhihong Li(zhihongli@bennington.edu)
	Date: 4/8/2020
"""
import socket

TCP_ADDRESS = '0.0.0.0' # listen to all ip address
TCP_PORT = 9000
BUFFER_SIZE = 512 # normal 1024 but we want fast response
MESSAGE_LIMIT = 4 
IP_ADDR_LENGTH = 15

# create a TCP (stream) socket using tcp-ip (INET)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((TCP_ADDRESS, TCP_PORT))
sock.listen(999)

print("Start Listening...")
while True:

# when connection is accepted,
# we get conn id and Ip of the remote host.
	conn, addr = sock.accept()
	print("Connection address: {0}".format(addr[0]))
	
# read data until there is no data left 
	new_msg = True
	receiver_ip = ""
	full_data = ""
	success_message = "success".encode()
	while True: 
		if new_msg:
			msg_length = conn.recv(MESSAGE_LIMIT).decode()
			msg_length = int(msg_length)	
			print("received msg length:" , msg_length)
			receiver_ip = conn.recv(IP_ADDR_LENGTH).decode()
			if receiver_ip != "":
				receiver_ip = receiver_ip.strip()
				print("receiver ip: " + receiver_ip)
			new_msg = False	
		data = conn.recv(BUFFER_SIZE).decode()
		#print("received data: ", data)
		full_data += data
		if len(full_data) == msg_length:
			conn.send(success_message)
			break
	print(full_data)
	conn.close()



# how data is received from server side. (#buffer)
# referece: https://www.youtube.com/watch?time_continue=779&v=Lbfe3-v7yE0&feature=emb_logo