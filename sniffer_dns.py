#!/usr/bin/env python3
import argparse, signal, sys, time
from banners import skull_banner, dns_sniffer_banner
import scapy.all as scapy
from termcolor import colored
from datetime import datetime

# Ctrl + c
def ctrl_c(sig, frame):
    print(colored("\n\n\t[!] Quiting...\n\n", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

# Get Actual time
def actual_time():
    now_time = str(datetime.now()).split('.')[0]
    return now_time

# Global Vars
dobliuw = colored("Dobliuw DNS Sniffer", 'red')
url = colored('https://github.com/Dobliuw/MyHackingTools', 'blue')
info = colored("[i]", 'yellow')
succes = colored("[+]", "green")
err = colored("[!]", 'red')
consulted_str = colored('consulted', 'green')
ip_regex = r'^(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?$'
mac_regex = r'^([a-fA-F0-9]{2}\:){5}([a-fA-F-0-9]{2})$'
mac_address = ""
domains_visiteds = set()

# Flags panel
def get_arguments():
    parser = argparse.ArgumentParser(description="DNS Sniffer ☠︎︎")
    # parser.add_argument("-t", "--target", required=True, dest="target_ip", help="Host or Host range to Spoof")
    # parser.add_argument("-g", "--gateway", required=True, dest="gateway", help="Default Gateway (Probably router IP)")
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Network Interface")
    args = parser.parse_args()

    return args.interface


def procces_dns_packet(packet):
    if packet.haslayer(scapy.DNSQR):
        domain = packet[scapy.DNSQR].qname.decode()
        if domain not in domains_visiteds:
            domains_visiteds.add(domain)
            print("%s Domain - %s" % (colored(domain, "blue"), consulted_str))

# Traffic sniffer
def sniff_traffic(interface):
    try:
        scapy.sniff(iface=interface, filter="udp and port 53", prn=procces_dns_packet, store=0) # Store = 0 (Not save packets)
    except:
        pass


# Start sniffer
if __name__ == "__main__":
    interface = get_arguments()
    skull_banner()
    time.sleep(1)
    dns_sniffer_banner()
    now = actual_time()
    print(f"Starting {dobliuw} v1.0 ( {url} ) at {now}\n") 
    print("\n\t%s Sniffing DNS Traffic for %s network interface...\n" % (info, colored(interface, "yellow")))
    sniff_traffic(interface)
