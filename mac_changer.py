#!/usr/bin/env python3
import argparse, signal, re, subprocess, sys, os, time
from termcolor import colored
from datetime import datetime
from banners import mac_changer_banner

# Ctrl + c
def ctrl_c(sig, frame):
    print(colored("\n\n\t[!] Quiting...\n\n", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

# Global Vars
dobliuw = colored("Dobliuw Macchanger", 'red')
url = colored('https://github.com/Dobliuw/MyHackingTools', 'blue')

# Get Actual time
def actual_time():
    now_time = str(datetime.now()).split('.')[0]
    return now_time

# Validate interface and mac address
def validate(i, m):
    valid_interface = re.match(r'^[e][n|t][s|h]\d{1,2}$', i)
    valid_mac = re.match(r'^([A-Fa-f0-9]{2}[:]){5}([A-Fa-f0-9]{2})$', m)

    return True if valid_interface and valid_mac else False

# Flags panel
def get_arguments():
    parser = argparse.ArgumentParser(description="Change MAC address for a network interface")
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Name of the network interface")
    parser.add_argument("-m", "--mac", required=True, dest="mac_address", help="The new MAC of the interface")
    args = parser.parse_args()
    return args.interface, args.mac_address

# Change the mac
def macchanger(interface, mac_address):
    
    mac_changer_banner()
    time.sleep(0.5)
    now = actual_time()    
    print(f"Starting {dobliuw} v1.0 ( {url} ) at {now}")
    start_time = time.time()    

    if validate(interface, mac_address):
        print("\n\t%s Trying to change the current mac to %s in interface %s...\n" % (colored("[i]", "yellow"), colored(mac_address, 'yellow'), colored(interface, 'yellow')))
        colored_interface = colored(interface, 'blue')
        colored_mac_address = colored(mac_address, 'blue')
        try:
            subprocess.run(["ifconfig", interface, "down"])
            subprocess.run(["ifconfig", interface, "hw", "ether", mac_address])
            subprocess.run(["ifconfig", interface, "up"])
            print("%s Mac successfully changed\n\n\t%s Listing interface %s...\n" % (colored('[+]', 'green'), colored('[i]', 'yellow'), colored_interface))
            stdout = subprocess.run(["ifconfig", interface], capture_output=True).stdout.decode()
            stdout = stdout.replace(interface, colored_interface).replace(mac_address, colored_mac_address)
            print(stdout)
            end_time = time.time()
            print(f"{dobliuw} v1.0 done: 1 MAC address ({colored_mac_address}) changed in {round(end_time - start_time, 2)} seconds")
        except:
            print(colored("\n\n\t[!] An error ocurred", "red"))
            sys.exit(1)

# Start the program
if __name__ == "__main__":
    if os.getuid() == 0:
        interface, mac_address = get_arguments()
        macchanger(interface, mac_address)
    else: 
        print(colored("\n\n\t[!] This script needs to be run as sudo ツ.\n\n", "red"))
        sys.exit(1)