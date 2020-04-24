#!/usr/bin/env python3
"""
	client.py = TCP chat app client that talks to a remote server on port 9000 and
		    sends accustomed message to another online client.
	Author: Zhihong Li(zhihongli@bennington.edu)
	Date: 4/8/2020
"""

import socket
import time
import threading

class SendMessage(threading.Thread):
	# initializer (constructor)
	def __init__(self, server_ip, tcp_port):
		threading.Thread.__init__(self)
		self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_ip = server_ip
		self.tcp_port = tcp_port
		self.msg = None
		self.msg_length = None
		self.receiver_ip = None
		self.data = None

	def get_receiver_ip_addr(self):
		self.receiver_ip = None
		receiver_ip_is_valid = False
		while receiver_ip_is_valid == False:
			self.receiver_ip = input("Enter the the message receiver's ip address:\n")
			for ip_block in self.receiver_ip.split("."):
				if ip_block.isdigit():
					if int(ip_block) <= 255:
						receiver_ip_is_valid = True
					else:
						print("Please enter the correct ip address")
						receiver_ip_is_valid = False
						break
				else:
					print("Please enter the correct ip address")
					receiver_ip_is_valid = False
					break
		self.receiver_ip = f"{self.receiver_ip:<15}"

	def get_msg_n_msgLength(self):
		self.msg = input("Enter the message you want to send:\n")
		while self.msg == "":
			self.msg = input("Enter the message you want to send:\n")
		self.msg_length = f"{len(self.msg):<{MESSAGE_LIMIT}}"

	def send_msg_to_server(self):
		#next, connect to the remote IP on the given port and send msg
		try:
			self.tcp_socket.settimeout(5)
			self.tcp_socket.connect((self.server_ip, self.tcp_port))
			self.tcp_socket.send(self.data)
			server_response = self.tcp_socket.recv(7).decode()
			if server_response == "success":
				print("\n-----------------------------------------------------------------")
				print("your successfully sent {0}: {1}".format(self.receiver_ip.strip(), self.msg))
				print("-----------------------------------------------------------------")
			else:
				print("failed to send the message, please try again")
		except:
			print("connection Failed")
		self.tcp_socket.close()

	def run(self):
		while True:
			self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # important
			self.get_receiver_ip_addr()
			self.get_msg_n_msgLength()
			self.data = self.msg_length + self.receiver_ip + self.msg
			self.data = self.data.encode()
			self.send_msg_to_server()
			time.sleep(0.5)


class ReceiveMessage(threading.Thread):
	def __init__(self, receive_msg_sock):
		threading.Thread.__init__(self)
		self.receive_msg_sock = receive_msg_sock
		self.receiver_ip = None

	def receive_msg_from_server(self):
		conn, addr = self.receive_msg_sock.accept()
		print("Connection address: {0}".format(addr[0]))

		# read data until there is no data left 
		new_msg = True
		self.receiver_ip = ""
		full_data = ""
		success_message = "success".encode()
		while True:
			if new_msg:
				msg_length = conn.recv(MESSAGE_LIMIT).decode()
				msg_length = int(msg_length)
				full_data += f"{msg_length:<{MESSAGE_LIMIT}}"
				print("received msg length:", msg_length)

				self.receiver_ip = conn.recv(IP_ADDR_LENGTH).decode()
				full_data += f"{self.receiver_ip:<{IP_ADDR_LENGTH}}"
				self.receiver_ip = self.receiver_ip.strip()
				print("receiver ip: " + self.receiver_ip)
				new_msg = False

			data = conn.recv(BUFFER_SIZE).decode()
			full_data += data
			if (len(full_data) - MESSAGE_LIMIT - IP_ADDR_LENGTH) == msg_length:
				conn.send(success_message)
				break
		print("---------------------------------------------------------------")
		print("Message received from {0}:\n{1}".format(self.receiver_ip, full_data[MESSAGE_LIMIT + IP_ADDR_LENGTH:]))
		print("---------------------------------------------------------------\n")
		conn.close()


	def run(self):
		while True:
			self.receive_msg_from_server()


if __name__ == "__main__":
	#configuration
	TCP_ADDRESS =  "127.0.0.1" # server address 
	LISTEN_ADDRESS = "0.0.0.0"
	TCP_PORT = 9000
	BUFFER_SIZE = 512
	MESSAGE_LIMIT = 4
	TCP_RECEIVE_PORT = 9001
	IP_ADDR_LENGTH = 15

	# receive message from server config
	receive_msg_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	receive_msg_sock.bind((LISTEN_ADDRESS,TCP_RECEIVE_PORT))
	receive_msg_sock.listen(99)

	#create class instance
	receive_msg = ReceiveMessage(receive_msg_sock)
	send_msg = SendMessage(TCP_ADDRESS, TCP_PORT)

	print("start receiving messages")
	receive_msg.start()
	send_msg.start()


			
# break only break out of a loop, it does not apply to if statement.
# reference: https://forums.coronalabs.com/topic/29138-how-to-break-out-of-an-if-statement/
# how to handle a socket timeout
# reference: https://kite.com/python/examples/5615/socket-handle-a-socket-timeout
# how to run two while loop at the same time
# reference: https://stackoverflow.com/questions/18773474/simple-way-to-run-two-while-loops-at-the-same-time-using-threading
