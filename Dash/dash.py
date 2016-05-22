#python 2.x

#Run macProbe.py first to determine MAC address
#To connect a DASH up to WiFi, follow
#www.amazon.com/dashbuttonsetup

#sudo apt-get install -y tcpdump
#sudo apt-get install -y socket
#sudo apt-get install -y time
#Run this as sudo (superuser)
#>sudo python dash.py &

import socket
import struct
import binascii
import requests
import time

# using belkin as my router
#
macAddr1 = '74c246731626'
macAddr2 = 'a002dc0b9827'

# Might need to update this once in a while
#
url = 'http://api.cloudstitch.io/flowersjsmccd/jefftesttwo/datasources/sheet'

rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))

#I like counters
#
i=0

def recordButton(unit):
    payLoad = {
        "Day":time.strftime("%A"),
        "Date":time.strftime("%Y-%m-%d"),
        "Time":time.strftime("%H:%M"),
        "Event":"Button UNIT %d Pressed" % unit,
        "Count":i,
        "IP": destIp
        }
    print "Button No. %d Pressed" % unit
    requests.post(url, payLoad)

    
while True:
    packet = rawSocket.recvfrom(2048)
    
    ethernet_header = packet[0][0:14]
    ethernet_detailed = struct.unpack('!6s6s2s', ethernet_header)

    arp_header = packet[0][14:42]
    arp_detailed = struct.unpack('2s2s1s1s2s6s4s6s4s', arp_header)

# skip non-ARP packets
    ethertype = ethernet_detailed[2]
    if ethertype != '\x08\x06':
        continue

    sourceMac = binascii.hexlify(arp_detailed[5])
    destIp = socket.inet_ntoa(arp_detailed[8])

    if sourceMac == macAddr1:
        unit = 1
        recordButton(unit)
        i += 1
    elif sourceMac == macAddr2:
        unit = 2
        recordButton(unit)
        i += 1
        
