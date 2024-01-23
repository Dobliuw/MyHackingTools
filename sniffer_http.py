#!/usr/bin/env python3
import argparse, signal, sys, time, os
from banners import skull_banner, http_sniffer_banner
import scapy.all as scapy
from scapy.layers import http
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
dobliuw = colored("Dobliuw HTTP Sniffer", 'red')
url = colored('https://github.com/Dobliuw/MyHackingTools', 'blue')
info = colored("[i]", 'yellow')
succes = colored("[+]", "green")
err = colored("[!]", 'red')
consulted_str = colored('consulted', 'green')
ip_regex = r'^(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?$'
mac_regex = r'^([a-fA-F0-9]{2}\:){5}([a-fA-F-0-9]{2})$'
mac_address = ""
urls_visiteds = set()

# Flags panel
def get_arguments():
    parser = argparse.ArgumentParser(description="HTTP Sniffer ☠︎︎")
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Network Interface")
    args = parser.parse_args()

    return args.interface


# Process packets
def procces_http_packet(packet):

    possible_creds = ["login", "user", "pass", "username", "password", "admin", "name", "uname", "pwd", "email", "mail", "correo", "urname"]

    if packet.haslayer(http.HTTPRequest):
        method = colored(packet[http.HTTPRequest].Method.decode(), "blue")
        url = f"http://{packet[http.HTTPRequest].Host.decode()}/{packet[http.HTTPRequest].Path.decode()} - {method}"
        
        if url not in urls_visiteds:
            urls_visiteds.add(url)
            print(url)

        if packet.haslayer(scapy.Raw):
            body = packet[scapy.Raw].load.decode()
            for word in possible_creds:
                if word in body:
                    print(colored(f"\n\t[!] Possible sensible data: {body}\n", 'yellow'))
                    break


# Traffic sniffer
def sniff_traffic(interface):
    try:
        scapy.sniff(iface=interface, prn=procces_http_packet, store=0) # Store = 0 (Not save packets)
    except Exception as e:
        print(e)


# Start sniffer
if __name__ == "__main__":
    if os.getuid() == 0:
        interface = get_arguments()
        skull_banner()
        time.sleep(1)
        http_sniffer_banner()
        now = actual_time()
        print(f"Starting {dobliuw} v1.0 ( {url} ) at {now}\n") 
        print("\n\t%s Sniffing HTTP Traffic for %s network interface...\n" % (info, colored(interface, "yellow")))
        sniff_traffic(interface)
    else:
        print(colored("\n\n\t[!] You need run this script like sudo.\n\n", "red"))
        sys.exit(1)