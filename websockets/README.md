# Quix WSI (WebSockets Interface)
### Authentication
Quix WSI performs simple authentication on the client-side using basic username/password authentication. The credentials are checked on the server and a token is provided to the user for future use.

#### Client
```js
{
    "auth": null,
    "req": "authenticate",
    "rid": 12345,
    "msg": {
        "username": "quix123",
        "password": "bright01"
    }
}
```

#### Server Response
```js
{
    "rid": 12345,
    "msg": {
        "success": true,
        "token": "fonsdkosdg9wjttj092gf1rj9fm2fe",  // To be used in the "auth" field on the client
        "validity": 86400,                          // Token lifetime (seconds)
    }
}

/* Failure Case */

{
    "rid": 12345,
    "msg": {
        "success": false,
        "reason": "password_invalid",
    }
}
```

# Process Handling
Note: Ideally, these operations should be performed by a user with access to only the Quix data folder, to prevent malicious scripts from reading data outside the Quix folder.

### Run application
#### Server
```js
{
    "req": "execute",
    "rid": 65019,
    "msg": {
        "bin": "python3",                       // binary to use (leave blank for system)
        "loc": "testserver/testserver.py",      // file location (relative to quix folder)
        "args": "--help"                        // command line arguments
    }
}
```

#### Client
```js
{
    "rid": 65019,
    "msg": {
        "result": "success",
        "proc_id": 12345                        // process ID for reference
    }
}
```

### View running applications
#### Server
```js
{
    "req": "view_running",
    "rid": 14791,
    "msg": {
        "verb": 1,      // Verbosity, placeholder
    }
}
```

#### Client
```js
{
    "rid": 14791,
    "msg": {
        [
            {
                "title": "Test Server v0.1",                        // Process Title
                "pid": 12351,                                       // Process ID
                "cpu_util": 0,                                      // %
                "mem_util": 111,                                    // MB
                "reqc": "python3 testserver/testserver.py --help",  // Run command
                "port_util": [12345, 56193]                         // Open ports for this process
            }
            // If more programs are running, they will be listed in this format.
        ]
    }
}
```

### Kill running application
Note: Only allow applications originally called by Quix Server to be terminated.

#### Server
```js
{
    "req": "proc_signal",
    "rid": 30491,
    "msg": {
        "pid": 12351,       // Process ID
        "mode": "SIGTERM"   // Kill mode (SIGTERM: soft, SIGKILL: hard, SIGHUP: graceful restart)
    }
}
```

#### Client
```js
{
    "rid": 30491,
    "msg": {
        "result": "success",
    }
}
```

# VPN Configuration
Quix WSI can send VPN configuration files to the client.

#### Client
```js
{
    "req": "get_vpn_conf",
    "rid": 45183,
    "msg": {
        "conf_type": "openvpn",
        "tun_mode": "udp"
    }
```

#### Server
```js
{
    "rid": 45183,
    "msg": {
        "result": "success",
        "conf_type": "openvpn",
        "conf_data": "dev tun\nproto udp ... ... ...-----END OpenVPN Static Key V1-----"
    }
}
```

# System statistics
### Telemetry
Quix Server can monitor vital statistics.  
The information required can be specified manually. In this case, all available options are specified.

#### Server
```js
{
    "req": "telemetry",
    "rid": 15185,
    "msg": {
        "stat_types" : ["ttl_cpu_usage", "ttl_mem_usage", "disk_util", "vpn_status"]
    }
}
```

#### Client
```js
{
    "rid": 15185,
    "msg": {
        "tele_data": {
            "ttl_cpu_usage": [0.10 0.11 0.02 0.01],     // % CPU usage of each core (0 ~ 1.00)
            "ttl_mem_usage": [128 1000 412],            // [Memory used, Buff/Cache, Free Memory]
            "disk_util": {
                "/dev/sda":  [195739194, 8185749375],   // [Bytes used, Bytes Free]
                "/dev/sdb":  [185844831, 8187395730]    // ^^
            },
            "vpn_status": {
                "ifname":    "tun0",                    // VPN Interface Name
                "conn_type": "openvpn",                 // VPN Connection Type
                "conn_host": "th1.s.quix.click",        // VPN Endpoint
                "conn_ip4":  "10.8.0.120",              // VPN IPv4 address
                "conn_ip6":  "fe80::1"                  // VPN IPv6 address
            }
        }
    }
}
```
