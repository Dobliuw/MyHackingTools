#!/usr/bin/env python3
import argparse, signal, re, os, sys, time, ipaddress, re
from concurrent.futures import ThreadPoolExecutor
from banners import arp_scan_banner
import scapy.all as scapy
from termcolor import colored
from datetime import datetime

# Ctrl + c
def ctrl_c(sig, frame):
    print(colored("\n\n\t[!] Quiting...\n\n", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

# Global Vars
dobliuw = colored("Dobliuw ARP Scanner", 'red')
url = colored('https://github.com/Dobliuw/MyHackingTools', 'blue')
info = colored("[i]", 'yellow')
succes = colored("[+]", "green")
err = colored("[!]", 'red')
found_str = colored('found', 'green')
ip_regex = r'^(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?$'
mac_regex = r'^([a-fA-F0-9]{2}\:){5}([a-fA-F-0-9]{2})$'
hosts_discovered = []

# Get Actual time
def actual_time():
    now_time = str(datetime.now()).split('.')[0]
    return now_time

# Flags panel
def get_arguments():
    parser = argparse.ArgumentParser(description="ARP host/s discovery IPv4")
    parser.add_argument("-t", "--target", required=True, dest="target_str", help="Give the host target or a network range to scan (-t 192.168.1.1 | -t 192.168.1.1/24)")
    parser.add_argument("--threads", dest="max_threads", help="Number of threads")
    
    args = parser.parse_args()

    return args.target_str, int(args.max_threads) if args.max_threads else 10

# Parse the target/s
def parse_target(target):
    if re.match(ip_regex, target):
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
        arp_layer_packet = scapy.ARP(pdst=host) # Protocol  Destination (pdst)
        ether_layer_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

        arp_packet = ether_layer_packet/arp_layer_packet # In scapy / is used to bind layers or protocols

        answered, _ = scapy.srp(arp_packet, timeout=2, verbose=False) # Send Recieve Packet (srp)

        for _, received_packet in answered:
            host_found = received_packet['ARP'].psrc
            hosts_discovered.append(host_found)
            print("%s %s (%s)" % (host_found, found_str, colored(received_packet['ARP'].hwsrc, 'yellow')))
    except Exception as e:
        print(e)


# Start Program
if __name__ == "__main__":

    if os.getuid() == 0:
        target_str, max_workers = get_arguments()
        targets = list(parse_target(target_str))
        max_workers = max_workers if max_workers > 0 and max_workers <= 500 else 10

        arp_scan_banner()  
        now = actual_time()
        print(f"Starting {dobliuw} v1.0 ( {url} ) at {now}\n")
        start_time = time.time()    
        
        if len(targets) == 1:
            print("\t%s Starting ARP scan for IP %s...\n" % (info, colored(targets[0], 'yellow')))
        else:
            print("\t%s Starting ARP scan from IP %s to IP %s...\n" % (info, colored(targets[0], 'yellow'), colored(targets[-1], 'yellow')))
            
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(host_discovery, targets)
        
        end_time = time.time()
        
        if len(hosts_discovered):
            print("\n%s Final %s hosts: %s" % (succes, found_str, colored(', '.join([str(port) for port in sorted(hosts_discovered)]), 'blue')))
        else:
            print("\n%s No hosts found." % (err))    
        print(f"\n{dobliuw} v1.0 done: {len(list(targets))} {'Host' if len(list(targets)) == 1 else 'Hosts'} scanned in {round(end_time - start_time, 2)} seconds")
    else:
        print(colored("\n\n\t[!] This script need runs like sudo.\n\n", "red"))
        sys.exit(1)