#!/usr/bin/env python3
import socket, signal, sys, argparse, time, os
from datetime import datetime
from termcolor import colored

# Global Vars
dobliuw = colored("Dobliuw Scan", 'red')
open_str = colored("open", 'green')
url = colored('https://github.com/dobliuw', 'blue')

# Ctrl + c
def ctrl_c(sig, frame):
    print(colored("\n\n\t[!] Quiting....\n\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

# Banner
def banner():
    print(colored("""
________        ___.   .__  .__               
\______ \   ____\_ |__ |  | |__|__ ____  _  ___
 |    |  \ /  _ \| __ \|  | |  |  |  \ \/ \/  /
 |    `   (  <_> ) \_\ \  |_|  |  |  /\      / 
/_______  /\____/|___  /____/__|____/  \_/\_/   Scan ツ ...
        \/           \/                       
""", 'red'))

# Get Actual time
def actual_time():
    now_time = str(datetime.now()).split('.')[0]
    return now_time

# Help pannel
def help(parser):
    parser.print_help()
    sys.exit(0)

# Get Arguments
def get_arguments():
    parser = argparse.ArgumentParser(description="Fast TCP Port Scanner")
    parser.add_argument("-t", "--target", dest="target", help="Victim target to scan (--target 192.168.1.1)")
    parser.add_argument("-p", "--port", dest="port", help="Port range to scan (--port 1-1000 / -p 21,22,80,443...)")
    parser.add_argument("-p-", "--allPorts", action='store_true', dest="all_ports", help="Scan the all 65535 ports")
    options = parser.parse_args()

    if options.target is None:
        help(parser)
    else:
        if options.all_ports is False and options.port is None:
            help(parser)
        else:
            if options.all_ports and options.port is None:
                return options.target, options.all_ports
            elif options.port and options.all_ports is False:
                return options.target, options.port
            else:
                help(parser)

# Create a socket connection
def create_socket():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.settimeout(1) # Try for 1 second if a port is open
    return soc

# Port Scanner
def port_scanner(host, port):
        soc = create_socket()

        try:    
            soc.connect((host, port))
            print(f"{port}/tcp {open_str}")
            soc.close()

        except (socket.timeout, ConnectionRefusedError):
            soc.close()    

# Start program
if __name__ == "__main__":
    try:
        target, port = get_arguments()

        banner()
        time.sleep(2)
        os.system('clear' if os.name == "posix" else 'cls')

        now = actual_time()
        print(f"Starting {dobliuw} v1.0 ( {url} ) at {now}")
        print("\n\t[i] Starting analysis for target %s...\n" % (colored(target, 'yellow')))

        time.sleep(0.5)

        print("\nPORT   STATE")

        start_time = time.time()

        if port == True:
            for port in range(1, 65535):
                port_scanner(target, port)
        elif '-' in port:
            ports = port.split('-')
            for port in range(int(ports[0]), int(ports[1])):
                port_scanner(target, port)
        elif ',' in port:
            ports = port.split(',')
            for port in ports:
                port_scanner(target, int(port))

        end_time = time.time()
        print(f"\n{dobliuw} v1.0 done: 1 IP address (1 host up) scanned in {round(end_time - start_time, 2)} seconds")
        sys.exit(0)

    except Exception as e:
        print(colored(f"\n\n\t[!] An error ocurred.\n\n {e}", 'red'))
        sys.exit(1)