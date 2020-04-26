# Server Side
server receives data in a format:

First 4 character - Length of the message to send

The Following 15 Characters - IP address of the receiver(if length of the ip is less than 15, fill up with space)

The rest characters will be the text message.

eg: (empty part is space) "6 255.255.255.255Hello!" "6 1.1.1.1 Hello!"

how server operates
After receiving full-data successfully, the server will reply "success" to the client to inform the client that the server has received the data successfully.

Next, the server will send the data to the receiver client via its IP addr sent by the sender.

Once the server sends the data to the receiver, it will receive response from receiver(client), if the response is "success", then this socket will close, connection with sender will also close. else. The server will print("failed to send the data to receiver").

The timeout is set to 5s, if the server does not hear response from the receiver in 5s, it will print "failed to send data to receiver.". then connection between sender and server will close.



# Client Side
Client will send data in a format as mentioned above, then wait for the server to respond 
"success". If the client receives "success" from server, it will continue to wait for the user to send another message.

On the other side, the client will forever listen to the server. 
Therefore, if the anyone send message to this client, it will receive the message and print it for the user.

# how to use it.

The user will be prompt to enter destination ip address,
And then it will prompt the user to enter message to send.
Then program will automatically packet the message in the format mentioned above and send it. 

# You can customize the server ip address in the client.py
