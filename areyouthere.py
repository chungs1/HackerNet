import os
import socket
import urllib2

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip

def gen_classC_ip_list(my_ip):
    last_octet = my_ip[my_ip.rfind('.') + 1:]
    trunc_ip = my_ip[:my_ip.rfind('.') + 1]
    return [trunc_ip + str(i) for i in range(1, 255)]

def find_local_nodes():
    my_ip = get_lan_ip()
    ip_list = gen_classC_ip_list(my_ip)
    found_nodes = []
    for ip in ip_list:
        print(ip)
        try:
            data = urllib2.urlopen("http://" + ip + ":1337/introduce", timeout = 0.25)
            if data.getcode() == 200 and data.read() == "HackerNet":
                found_nodes.append(ip)
                print("success!")
        except urllib2.URLError:
            pass
    return found_nodes
