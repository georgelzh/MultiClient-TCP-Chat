#!/usr/bin/env python3
"""
	server.py = TCP chat App server that listens all the clients' requests on port 8888.
	It helps the sender send messages to the receiver.
	Then it returns a "success" to sender. Then it prints the message that was sent.
	Author: Zhihong Li(zhihongli@bennington.edu)
	Date: 4/8/2020
"""
import socket

def server_handler(tcp_socket):
	conn, addr = tcp_socket.accept()
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
			full_data += f"{msg_length:<{MESSAGE_LIMIT}}"
			print("received message length:", msg_length)

			receiver_ip = conn.recv(IP_ADDR_LENGTH).decode()
			full_data += f"{receiver_ip:<{IP_ADDR_LENGTH}}"
			receiver_ip = receiver_ip.strip()
			print("receiver ip: " + receiver_ip)		
			new_msg = False

		data = conn.recv(BUFFER_SIZE).decode()
		full_data += data
		if (len(full_data) - MESSAGE_LIMIT - IP_ADDR_LENGTH) == msg_length:
			conn.send(success_message)
			pass_data_to_client(receiver_ip, TCP_RECEIVE_PORT, full_data.encode())
			break
	
	print("received data :", full_data)
	print("-----------------------------------------\n")
	conn.close()


def pass_data_to_client(receiver_ip, tcp_receive_port, data):
	tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_socket.settimeout(5)
	tcp_socket.connect((receiver_ip, tcp_receive_port))
	tcp_socket.send(data)
	server_response = tcp_socket.recv(7).decode()
	if server_response == "success":
		print("\n-----------------------------------------")
		print("successfully sent the message to", receiver_ip)

	else:
		print("failed to send the message, please try again")
	tcp_socket.close()


if __name__ == '__main__':
	TCP_ADDRESS = '0.0.0.0' # listen to all ip address
	TCP_PORT = 9000
	TCP_RECEIVE_PORT = 9000
	BUFFER_SIZE = 512 # normal 1024 but we want fast response
	MESSAGE_LIMIT = 4
	IP_ADDR_LENGTH = 15

	# create a TCP (stream) socket using tcp-ip (INET)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	sock.bind((TCP_ADDRESS, TCP_PORT))
	sock.listen(999)

	print("Start Listening...")
	while True:
		server_handler(sock)



# how data is received from server side. (#buffer)
# referece: https://www.youtube.com/watch?time_continue=779&v=Lbfe3-v7yE0&feature=emb_logo
# what leads to [Error 9] Bad file descriptor ? 
# reference https://stackoverflow.com/questions/7686275/what-can-lead-to-ioerror-errno-9-bad-file-descriptor-during-os-system
