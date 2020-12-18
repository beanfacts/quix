#!/usr/bin/env python

# WSS (WS over TLS) client example, with a self-signed certificate
import logging
import asyncio
import pathlib
import ssl
import websockets
import random
import os,binascii
import json
logging.basicConfig(filename='example.log', level=logging.INFO)

currentPrograms = [            {
                "title": "Test Server v0.1",                       # // Process Title
                "pid": 12321,                                       #// Process ID
                "cpu_util": 0,                                     # // %
                "mem_util": 111,                                    #// MB
                "reqc": "python3 testserver/testserver.py --help",  #// Run command
                "port_util": [12345, 56193]                         #// Open ports for this process
            },             {
                "title": "Test Server v0.2",                       # // Process Title
                "pid": 44421,                                       #// Process ID
                "cpu_util": 0,                                     # // %
                "mem_util": 111,                                    #// MB
                "reqc": "python3 testserver/testserver.py --help",  #// Run command
                "port_util": [12345, 56193]                         #// Open ports for this process
            }]

def random_hex():
    return str(binascii.b2a_hex(os.urandom(15))).replace('b','')

def random_digit():
    return random.randint(10000,99999)
def authentication(username,password):
    authentication = {
    "auth": None,
    "req": "authenticate",
    "rid": random_digit(),
    "msg": {
        "username": username,
        "password": password
    }
    }
    return json.dumps(authentication)

def authentication_token(token):
    authentication= {
    "auth": None,
    "req": "token_authentication",
    "rid": random_digit(),
    "msg": {
        "token_id": token
    }
    }
    return json.dumps(authentication)

def requestVpn(token, vpnType):
    result = {
    "token":token,
    "req": "get_vpn_conf",
    "rid": random_digit(),
    "msg": {
        "conf_type": vpnType,
        "tun_mode": "udp"
    } }
    return json.dumps(result)


def replyKillRunningApp(rid):
    result = {
    "rid": rid,
    "msg": {
        "result": "success",
    }
}
    return json.dumps(result)

def replySystemStats(rid):
    result = {
    "rid": rid,
    "msg": {
        "tele_data": {
            "ttl_cpu_usage": [0.10, 0.11, 0.02, 0.01],     #// % CPU usage of each core (0 ~ 1.00)
            "ttl_mem_usage": [128, 1000, 412],            #// [Memory used, Buff/Cache, Free Memory]
            "disk_util": {
                "/dev/sda":  [195739194, 8185749375],   #// [Bytes used, Bytes Free]
                "/dev/sdb":  [185844831, 8187395730]    #// ^^
            },
            "vpn_status": {
                "ifname":    "tun0",                    #// VPN Interface Name
                "conn_type": "openvpn",                 #// VPN Connection Type
                "conn_host": "th1.s.quix.click",        #// VPN Endpoint
                "conn_ip4":  "10.8.0.120",              #// VPN IPv4 address
                "conn_ip6":  "fe80::1"                  #// VPN IPv6 address
            }
        }
    }
}
    return json.dumps(result)
#data = [{"username": "quix123", "password": "bright01"}, {"username": "hello", "password": "bright01"}]
#data = {'quix123':'bright01', 'youyo123':'bright01', 'poiler33':'123hurrhr', 'poiler22':'bright01'}

def replyViewRunningApp(rid):
    result = {
    "rid": rid,
    "msg": {
        
           currentPrograms()
            #// If more programs are running, they will be listed in this format.
        
    }
}
    return json.dumps(result)

def replyRunningApp(rid):
    result = {
    "rid": rid,
    "msg": {
        "result": "success",
        "proc_id": 12345                      #  // process ID for reference
    }
}
    return json.dumps(result)

def currentRunningPrograms():
    return currentPrograms
#loginStatus =  False
async def hello():
    uri = "wss://th1.s.quix.click/oob/"
    async with websockets.connect(
        uri, ssl=True
    ) as websocket:
        try:
            with open('token.txt', 'r') as f:
                data = f.read()
                if len(data) != 0:
                    result = authentication_token(json.loads(data)['token'])
                    print(result)
                    await websocket.send(result)
                    print(data)
                else:
                    result = authentication_token("no token found") 
                    await websocket.send(result)
                while True:
                    try:
                        greeting = await websocket.recv()
                        print(f"< {(greeting)}")
                        
                    except ValueError:
                        greeting = await websocket.recv()
                        print(f"< {(greeting)}")  
        except FileNotFoundError:
            print("Wrong file or file path");
            f= open("token.txt","w+")


asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()
#print(random_hex())




