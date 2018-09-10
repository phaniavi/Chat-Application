#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import tkinter

def receive():
	while True:
		try:
			msg = client_socket.recv(BUF_SIZE).decode()
			msg_list.insert(tkinter.END, msg)
		except OSError:
			break

def send(event=None):
	msg = my_msg.get()
	my_msg.set('')
	client_socket.send(msg.encode())
	if msg == 'quit':
		client_socket.close()
		top.quit()

def on_closing(event=None):
	my_msg.set('quit')
	send()

top = tkinter.Tk()
top.title('Chat for Fun!')

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()		# For the messages to be sent
my_msg.set('Type your message here.')
scrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind('<Return>', send)
entry_field.pack()

send_button = tkinter.Button(top, text='SEND', command=send)
send_button.pack()

top.protocol('WM_DELETE_WINDOW', on_closing)

HOST = input('Enter Host: ')
PORT = input('Enter Port: ')

if not PORT:
	PORT = 5555
else:
	PORT = int(PORT)

BUF_SIZE = 2048
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

tkinter.mainloop()
