import pyroute2 as pr2
import ipaddress as ipa
import urllib.request as ureq
import logging
import json
import os, sys

from .addr import AddressPool

class Server:

    def __init__(self, raw_data: dict, local=True):
        """
        Attach server to a WireGuard interface.  
        If one does not exist, it will be created automatically.
        """

        # Store the raw data for later use
        self.raw_data = raw_data

        self.IPR = pr2.IPRoute()

        if local:
            self.NDB = pr2.NDB()
        else:
            db_spec = {
                "dbname":   self.raw_data["pg_dbname"],
                "host":     self.raw_data["pg_host"],
                "user":     self.raw_data["pg_user"],
                "password": self.raw_data["pg_pass"]
            }
            self.NDB = pr2.NDB(db_provider="psycopg2", db_spec=db_spec)

        self.ifname = self.raw_data["ifname"]

        if (self.iface_exists(self.ifname)
                and self.NDB.interfaces[self.ifname]['kind'] == 'wireguard'):
            print("A WireGuard interface already exists. Skipping configuration steps.")
        else: 
            # Create a WireGuard Interface given the parameters
            
            self.wgif = self.NDB.interfaces.create(
                kind="wireguard", 
                ifname=self.ifname)
            
            # Add an address to the newly created WireGuard interface
            self.wgif.add_ip(self.raw_data["gateway_ip"])

            # Attempt to commit our WireGuard changes first
            try:
                self.wgif.set("state", "up")
                self.wgif.commit()
            except pr2.netlink.exceptions.NetlinkError as e:
                print("Netlink Error:", e.args[1])
                diag = {
                    0: "Linux headers and/or WireGuard may not be installed.",
                    1: "This program must be run as root."
                }
                if e.code in diag:
                    print(diag[e.code])
                else:
                    print("No troubleshooting information was found.")

        # Attempt to start the WireGuard server on the listening port
        # specified in the configuration file.
        self.wgtool = pr2.WireGuard()
        self.wgtool.set(
            self.ifname,
            self.raw_data["listen_port"],
            0x6969,
            self.raw_data["private_key"]
        )

        # Find the public IP address of this server.
        # Note that IPv6 functionality is not yet tested.
        if "public_ip" not in raw_data:
            a = self.find_public_ip()
            print(a)
    
        # Create an address pool for the WireGuard interface.
        x = self.get_ifaddr(self.ifname)
        self.apool = AddressPool(x[0], x[1])

    @staticmethod
    def iface_exists(name: str):
        """
        Check if an interface exists.
        """
        ipr = pr2.IPRoute()
        irlink = ipr.link_lookup(ifname=name)
        return len(irlink)
        
    @staticmethod
    def get_ifaddr(name: str):
        ipr = pr2.IPRoute()
        irlink = ipr.link_lookup(ifname=name)
        ip, pl = None, None
        if len(irlink) == 1:           
            ir_detail = ipr.get_addr(index=irlink[0])
            if len(ir_detail) == 0:
                print("Could not find an address!")
                return (None, None)
            elif len(ir_detail) > 1:
                print("More than 1 assigned address.")
            ir_detail = ir_detail[0]
            pl = ir_detail['prefixlen']
            for pair in ir_detail['attrs']:
                print(">", pair)
                if pair[0] == "IFA_ADDRESS":
                    ip = pair[1]
                    break
        print("ip/pl =", ip, pl)
        return (ip, pl)
    
    def find_public_ip(self):
        """ If the server is behind NAT with a port forwarding rule, this
            function finds the public IP address of the default gateway. """  
        a = ureq.Request('https://ifconfig.co')
        a.add_header('User-Agent', 'curl')
        resp = ureq.urlopen(a)
        if resp.code == 200 and 0 < resp.length < 100:
            pub_addr = resp.read().decode('utf-8').rstrip()
            print("pub addr:", pub_addr)
            try:
                return ipa.ip_address(pub_addr)
            except ValueError:
                print("Error getting public address.")
        print("Determining public address.")
    
    def get_gw_ip(self):
        """ Retrieve the WireGuard interface IP address and netmask
            in string format. """
        return self.wg_ip[0] + "/" + self.wg_ip[1]

    def check_peer_exists(self, pub_key):
        wg_attr = self.wgtool.info(self.ifname)[0]['attrs']
        for attr in wg_attr:
            if attr[0] == 'WGDEVICE_A_PEERS':
                for peer in attr[1]:
                    for i in peer['attrs']:
                        if i[0] == 'WGPEER_A_PUBLIC_KEY':
                            if i[1].decode("ascii") == pub_key:
                                return True
        return False

    def add_peer(self, pub_key, ka=10):
        newpeer = {
            "public_key": pub_key,
            "persistent_keepalive": ka,
            "allowed_ips": [self.apool.allocate_ip()],
            "allowed_routes": [self.apool.server_address_string()]
        }
        print("New Peer:\n", newpeer)
        self.wgtool.set(self.ifname, peer=newpeer)
        print(self.wgtool.info(self.ifname))