#!/usr/bin/env python3
"""
	client.py = TCP chat app client that talks to a remote server on port 9000 and
		    sends accustomed message to another online client.
	Author: Zhihong Li(zhihongli@bennington.edu)
	Date: 4/8/2020
"""

import socket
import time

BUFFER_SIZE = 1024
TCP_ADDRESS =  "10.10.248.89" # server address
TCP_PORT = 9001
MESSAGE_LIMIT = 4

while True:
	receiver_ip = "127.0.0.1"
	# receiver_ip_is_valid = False
	# text = None
	# while receiver_ip_is_valid == False:
	# 	receiver_ip = input("Enter the the message receiver's ip address:\n")
	# 	for ip_block in receiver_ip.split("."):
	# 		if ip_block.isdigit():
	# 			if int(ip_block) <= 255:
	# 				receiver_ip_is_valid = True
	# 			else:
	# 				print("Please enter the correct ip address")
	# 				receiver_ip_is_valid = False
	# 				break
	# 		else:
	# 			print("Please enter the correct ip address")
	# 			receiver_ip_is_valid = False
	# 			break


	# for server to identity the ip address, we fix the lenth of receiver_ip to 15 digits
	if (len(receiver_ip) < 15):
		receiver_ip += " " *(15-len(receiver_ip))

	text = input("Enter the text you want to send:\n")
	while text == "":
		text = input("Enter the text you want to send:\n")

	msg_length = f"{len(text):<{MESSAGE_LIMIT}}"	
	MESSAGE = msg_length + receiver_ip + text

	# first create the socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#next, connect to the remote IP on the given port
	try:
		sock.settimeout(5)
		sock.connect((TCP_ADDRESS, TCP_PORT))
		sock.send(MESSAGE.encode())
		# server_response = sock.recv(7).decode()
		# if server_response == "success":
		# 	print(server_response)
		# 	continue
		# else:
		# 	print("failed to send the message, please try again")
	except:
		print("connection Failed")
	sock.close()

