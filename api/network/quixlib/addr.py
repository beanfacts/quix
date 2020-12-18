import pyroute2 as pr2
import ipaddress as ipa
import urllib.request as ureq
import logging
import json
import os, sys

class AddressPool:

    def __init__(self, server_addr: str, server_mask: int):
        """
        Generate an address pool using the server address and its subnet mask.
        """
        self.server_addr = ipa.IPv4Address(server_addr)
        self.network = ipa.IPv4Network(
            str(server_addr) + '/' + str(server_mask), strict=False)
        
        self.reserved_pool = {
            self.server_addr.compressed: {
                "type": "server",
                "meta": "WireGuard Gateway"
            }
        }
    
    def check_addr_valid(self, addr):
        return (
            (addr in self.network)
            and (addr != self.network.network_address)
            and (addr != self.network.broadcast_address)
        )
    
    def add_addr(self, new_addr: ipa.IPv4Address, meta=None):
        """
        Add a new address assignment.
        """
        if self.check_addr_valid(new_addr) and (new_addr not in self.reserved_pool):
            self.reserved_pool[new_addr.compressed] = {
                "type": "client",
                "meta": meta
            }
            print("Lease created.")

    def remove_addr(self, addr):
        """
        Remove the specified address from the pool.
        """
        del self.reserved_pool[addr]

    def server_address_string(self):
        """ 
        Return the server address as a full IPv4 string literal including
        the /32 netmask.
        """
        return ipa.IPv4Network(self.server_addr).compressed

    def allocate_ip(self):
        """
        Allocate an IP address sequentially.
        Note: IPv4 subnet size must be /30 or larger.
        """
        for ip in self.network.hosts():
            if ip.compressed not in self.reserved_pool:
                self.add_addr(ip, "test user")
                return ip.compressed + "/32"

    def import_existing(self):
        """
        Import the existing address assignments from the WireGuard server.
        """
        pass