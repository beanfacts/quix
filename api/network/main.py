import pyroute2 as pr2
import ipaddress as ipa
import urllib.request as ureq
import logging
import json
import os, sys

from quixlib.server import Server

"""
10.148.0.4:5432
    u: postgres
    p: bobandyui.com
"""

if os.getuid() != 0:
    print("Not running as root!")
    sys.exit(1)


def import_server_config(fname="conf.json"):
    if os.path.isfile(fname):
        with open(fname, "r") as f:
            data = json.load(f)
            print(data)
            return data
    return None

a = Server(import_server_config(), False)
a.add_peer("rbX3e6vz5T32y50UhPRDrjzC14sepAkfW96noddxsW0=", 5)
print("Peer exists:", a.check_peer_exists("rbX3e6vz5T32y50UhPRDrjzC14sepAkfW96noddxsW0="))
import code
code.interact(local=locals())