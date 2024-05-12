from scapy.all import * 
import signal, sys, readline, os

# Configuration 

readline.parse_and_bind("set editing-mode emacs")

# Ctrl + c

def ctrl_c(sig, frame):
    print("\n\n\t[!] Quiting...\n\n")
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c) 

# Data exfiltration

def sniffTrafic(interface):
    print("\n[+] Your file content: \n")
    sniff(iface=interface, prn=readICMPpatterns)
    

def readICMPpatterns(packet): 
    
    if packet.haslayer(ICMP) and packet[ICMP].type == 8:
        line = packet[ICMP].load[-4:].decode('utf-8')
        print(line, flush=True, end='')


if __name__ == "__main__": 
    
    if os.geteuid() == 0:
        interface = input("\n\t[!] Please insert the interface to listen: ")
        sniffTrafic(interface) 
    else: 
        print("\n\n\t[!] Please run the script as root ツ\n\n")
