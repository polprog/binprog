#!/usr/bin/env python3
import socket


def dns_lookup(address):
    try:
        ipaddrs = [ str(i[4][0]) for i in socket.getaddrinfo(address, 0) ]
    except OSError as e:
        return "E005 " + str(e.strerror) 

    ipaddrs = list(dict.fromkeys(ipaddrs))
    if len(ipaddrs) > 4:
        return ", ".join(ipaddrs[:4]) + " and " + str(len(ipaddrs) - 4) + " more."
    else:
        return ", ".join(ipaddrs)

def rdns_lookup(address):
    try:
        return str(socket.gethostbyaddr(address)[0])
    except OSError as e:
        return "E005 " + str(e.strerror) 
        

if __name__ == "__main__":
    print(dns_lookup("google.com"))
    print(dns_lookup("a.root-servers.net"))
    print(rdns_lookup("8.8.8.8"))
    print(rdns_lookup("Not an IP address"))
