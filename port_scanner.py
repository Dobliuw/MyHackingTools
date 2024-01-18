#!/usr/bin/env python3
import socket, signal, sys, argparse, time, threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from termcolor import colored

# Global Vars
dobliuw = colored("Dobliuw Scan", 'red')
open_str = colored("open", 'green')
url = colored('https://github.com/Dobliuw/MyHackingTools', 'blue')
open_sockets = []
open_ports_finded = []

# Ctrl + c
def ctrl_c(sig, frame):
    for soc in open_sockets:
        soc.close()
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
""", 'green'))

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
    parser.add_argument("-t", "--target", dest="target", required=True, help="Victim target to scan (--target 192.168.1.1)")
    parser.add_argument("-p", "--port", dest="port", help="Port range to scan (--port 1-1000 / -p 21,22,80,443...)")
    parser.add_argument("-p-", "--allPorts", action='store_true', dest="all_ports", help="Scan all 65535 ports")
    parser.add_argument("-sh", "--show-headers", action='store_true', dest="show_headers", help="Make an HTTP request to try see the Headers Service Response")
    parser.add_argument("--threads", dest="max_threads", help="Number of threads")
    options = parser.parse_args()

    if options.all_ports is False and options.port is None:
        help(parser)
    else:
        if options.all_ports and options.port is None:
            return options.target, options.all_ports, int(options.max_threads) if options.max_threads else 0, options.show_headers
        elif options.port and options.all_ports is False:
            return options.target, options.port, int(options.max_threads) if options.max_threads else 0, options.show_headers
        else:
            help(parser)

# Create a socket connection
def create_socket():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.settimeout(3) # Try for 1 second if a port is open
    open_sockets.append(soc)
    return soc

# Port Scanner
def port_scanner(host, port, show_headers):
        soc = create_socket()

        try:    
            soc.connect((host, port))
            soc.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            open_ports_finded.append(port)

            if show_headers:
                header = soc.recv(1024).decode(errors='ignore') # Get Headers
                if header:
                    print(f"{port}/tcp {open_str}")
                    print(colored(f"\n{header}\n", 'white'))
                else:
                    print(f"{port}/tcp {open_str}")
            else: 
                print(f"{port}/tcp {open_str}")

        except (socket.timeout, ConnectionRefusedError):
            pass

        finally:
            soc.close()

# Return ports 
def port_parser(port_str):
    if port_str == True:
        return range(1, 65535)
    elif '-' in port_str:
        start, end = map(int, port_str.split('-'))
        return range(start, end+1)
    elif ',' in port_str:
        return map(int, port_str.split(','))
    else:
        return [int(port_str)]

        
# Start program
if __name__ == "__main__":
    try:
        target, ports, thread, show_headers = get_arguments()
        max_workers = thread if thread > 0 and thread <= 500 else 10 
        banner()
        now = actual_time()
        
        print(f"Starting {dobliuw} v1.0 ( {url} ) at {now}")
        print("\n\t%s Starting analysis for target %s...\n" % (colored("[i]", "yellow"), colored(target, 'yellow')))

        time.sleep(1)


        print("\nPORT   STATE")

        start_time = time.time()

        # Execute a function with limit threads (map recieve 1 args if u send 1 iterable, 2 if u send 2....)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(lambda port: port_scanner(target, port, show_headers), port_parser(ports))

        end_time = time.time()
        print("\n%s Final %s ports: %s" % (colored('[+]','green'),open_str, colored(', '.join([str(port) for port in sorted(open_ports_finded)]), 'blue')))
        print(f"\n{dobliuw} v1.0 done: 1 IP address (1 host up) scanned in {round(end_time - start_time, 2)} seconds")
        sys.exit(0)

    except Exception as e:
        print(colored(f"\n\n\t[!] An error ocurred.\n\n {e}", 'red'))
        sys.exit(1)