# Quix Client REST API
&nbsp; 
### Authenticate  
-----------------------------
&nbsp;
Client  
```
POST /api/v1/client/auth
```
```js
{
    "username": "quix123",
    "password": "bright01"
}
```
&nbsp;
Server Response  
```js
{
    "token": "fonsdkosdg9wjttj092gf1rj9fm2fe",
    "valid": 86400
}
```
&nbsp; 
### Get Backends
-----------------------------
Client  
```
GET /api/v1/client/backends
Content-Type: application/json
Authorization: Bearer <token>
```
Response
```js
{
    "msg": [
        {
            "id": 1,
            "name":     "Bob's Server",
            "uplink":   "th1.s.quix.click",
            "status":   "ok",
            "location": "BKK"
        },
        {
            "id": 2,
            "name":     "Game Server",
            "uplink":   "th1.s.quix.click",
            "status":   "ok",
            "location": "BKK"
        }
    ]
}
```
&nbsp; 
### Get Backend Detail
-----------------------------
```
GET /api/v1/client/backends?id=1
Content-Type: application/json
Authorization: Bearer <token>
```
Response
```js
{
    "name": "Bob's Server",
    "uplink": "th1.s.quix.click",
    "status": "ok",
    "location": "bkk",
    "internal_ip": "10.13.14.25",
    "rules": [
        {
            "ext_ip":   "1.2.3.4",
            "proto":    "TCP",
            "eport":    9999,
            "iport":    4444
        },
        {
            "ext_ip":   "1.2.3.4",
            "proto":    "TCP",
            "eport":    9451,
            "iport":    4321
        }
    ]
}
```
&nbsp; 
### Update Backend Information
-----------------------------
Modifiable Parameters  

| Parameter   | Description             | CRUD | 
| ----------- | ----------------------- | ---- |
| `name`      | Server Friendly Name    | RU   | 
| `location`  | Server Uplink Location  | CRUD |
| `rules`     | Server Forwarding Rules | CRUD |

Rule Values

| Rule        | Description             | Acceptable Values      |
| ----------- | ----------------------- | ---------------------- |
| `ext_ip`    | External IP             | Any IPv4 host address  |
| `proto`     | Protocol                | TCP, UDP               |
| `port`      | External Port           | 0 ~ 65535              |
| `iport`     | Internal Port           | 0 ~ 65535              |

Action Types
| Action         | Description                           |
| -------------- | ------------------------------------- |
| `create`       | Create a new key/value pair           |
| `delete`       | Delete a key/value pair               |
| `modify`       | Modify a modifiable key/value pair    |
| `delete_rule`  | Delete existing forwarding rule       |
| `create_rule`  | Create new forwarding rule            |
&nbsp; 
```
PATCH /api/v1/client/backends/modify?id=1
Content-Type: application/json
Authorization: Bearer <token>
```
```js
{
    "cmd": [
        {
            "op": "modify",
            "data": {
                "name": "Game Server"
            }
        },
        {
            "op": "delete",
            "keys": ["location"]
        }
        {
            "op": "delete_rule",
            "data": {
                "ext_ip": "1.2.3.4",
                "proto": "TCP",
                "eport": 9999,
                "iport": 4444
            }
        },
        {
            "op": "create_rule",
            "data": {
                "ext_ip": "1.2.3.4",
                "proto": "UDP",
                "eport": 9999,
                "iport": 4444
            }
        }
    ]
}
```
Response
The server should return the appropriate HTTP status code.
&nbsp; 
### Backend Token Generation
-----------------------------
```
GET /api/v1/client/pin?type=token
Content-Type: application/json
Authorization: Bearer <token>
```
Response
```js
{
    "pin":      "1dg9x1fz",
    "valid":    180
}
```
&nbsp;
### Backend Token Retrieval
-----------------------------
```
GET /api/v1/backend/token?pin=1dg9x1fz
Content-Type: application/json
```
Response
```js
{
    "token": "fonsdkosdg9wjttj092gf1rj9fm2fe",
    "valid": -1
}