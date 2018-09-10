#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

addresses = {}
clients = {}

HOST = ''
PORT = 5555
ADDR = (HOST,PORT)
BUF_SIZE = 2048

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():

	while True:
		client, client_address = SERVER.accept()	# client is the connection(client_socket) to the incoming client socket
		print('{}:{} has connected.'.format(client_address[0], client_address[1]))
		client.send('Greetings from the creator! Now type your name and press enter!'.encode())
		addresses[client] = client_address
		Thread(target=handle_client, args=(client,)).start()

def handle_client(client):	# Takes client socket as argument

	name = client.recv(BUF_SIZE).decode()
	welcome = 'Welcome {}! If you ever want to quit, type quit to exit.'.format(name)
	client.send(welcome.encode())
	msg = '{} has joined the chat!'.format(name)
	broadcast(msg.encode())
	clients[client] = name

	while True:
		msg = client.recv(BUF_SIZE)
		if msg != 'quit'.encode():
			broadcast(msg, '{}: '.format(name).encode())
		else:
			client.send(bytes('quit', 'utf-8'))
			client.close()
			del clients[client]
			broadcast('{} has left the chat.'.format(name).encode())
			break

def broadcast(msg, prefix=''):
	for sock in clients:
		sock.send('{} {}'.format(prefix.decode(),msg.decode()).encode())

if __name__ == '__main__':
	SERVER.listen(5)	# Max 5 connections are allowed for communication with the server after that connections are blocked
	print('Waiting for connection......')
	ACCEPT_THREAD = Thread(target=accept_incoming_connections)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()
