#!/usr/bin/env python3
import argparse, signal, re, subprocess, sys, time, ipaddress, re
from concurrent.futures import ThreadPoolExecutor
from banners import icmp_scan_banner
from termcolor import colored
from datetime import datetime

# Ctrl + c
def ctrl_c(sig, frame):
    print(colored("\n\n\t[!] Quiting...\n\n", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

# Global Vars
dobliuw = colored("Dobliuw ICMP Scanner", 'red')
url = colored('https://github.com/Dobliuw/MyHackingTools', 'blue')
info = colored("[i]", 'yellow')
succes = colored("[+]", "green")
err = colored("[!]", 'red')
found_str = colored('found', 'green')
hosts_discovered = []


# Get Actual time
def actual_time():
    now_time = str(datetime.now()).split('.')[0]
    return now_time

# Flags panel
def get_arguments():
    parser = argparse.ArgumentParser(description="ICMP host/s discovery IPv4")
    parser.add_argument("-t", "--target", required=True, dest="target_str", help="Give the host target or a network range to scan (-t 192.168.1.1 | -t 192.168.1.1/24)")
    parser.add_argument("--threads", dest="max_threads", help="Number of threads")
    
    args = parser.parse_args()

    return args.target_str, args.max_threads if args.max_threads else 10

# Parse the target/s
def parse_target(target):
    if re.match(r'^(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?$', target):
        if '/' in target: 
            try:
                network = ipaddress.IPv4Network(target, strict=False)
                return map(str, network.hosts())
            except ipaddress.NetmaskValueError:
                print(colored("\n\n\t[!] Invalid Netmask\n\n", 'red'))
                sys.exit(1)
        elif '/' not in target:
            return [target]
    else:
        print(colored('\n\n\t[!] Invalid IP format: (Allowed formats: 192.168.1.1 - 192.168.1.1/24)\n\n'))
        sys.exit(1)

def host_discovery(host):

    try:
        ping = subprocess.run(["ping", "-c", "1", host], timeout=1, stdout=subprocess.DEVNULL)
        if ping.returncode == 0:
            print("%s  %s" % (host, found_str))
            hosts_discovered.append(host)
    except subprocess.TimeoutExpired:
        pass


# Start Program
if __name__ == "__main__":

    target_str, max_workers = get_arguments()
    targets = list(parse_target(target_str))
    max_workers = max_workers if max_workers > 0 and max_workers <= 500 else 10

    icmp_scan_banner()  
    now = actual_time()
    print(f"Starting {dobliuw} v1.0 ( {url} ) at {now}\n")
    start_time = time.time()    
    
    if len(targets) == 1:
        print("\t%s Starting scan for IP %s...\n" % (info, colored(targets[0], 'yellow')))
    else:
        print("\t%s Starting scan from IP %s to IP %s...\n" % (info, colored(targets[0], 'yellow'), colored(targets[-1], 'yellow')))
        
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(host_discovery, targets)
    
    end_time = time.time()
    
    if len(hosts_discovered):
        print("\n%s Final %s hosts: %s" % (succes, found_str, colored(', '.join([str(port) for port in sorted(hosts_discovered)]), 'blue')))
    else:
        print("\n%s No hosts found." % (err))    
    print(f"\n{dobliuw} v1.0 done: {len(list(targets))} {'Host' if len(list(targets)) == 1 else 'Hosts'} scanned in {round(end_time - start_time, 2)} seconds")