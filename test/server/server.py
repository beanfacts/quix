#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import secrets

import mysql.connector





logging.basicConfig()

STATE = {"value": 0}

USERS = set()
MAPPING_TOKEN_SOCKET = {}



def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

    
def random_hex():
    return secrets.token_hex(15)


tokens={}

def success_authentication(rid,token):
    #token = random_hex()
    #tokens[str(token)] = username
    result = {"rid": rid,"msg": {"success": True,"token": token,  "validity": 86400}}   
    return json.dumps(result)

def fail_authentication(rid):
    result = { "rid": rid, "msg": { "success": False, "reason": "token_invalid"} }
    return json.dumps(result)



async def brightRegister(websocket, token):
    MAPPING_TOKEN_SOCKET[token] = websocket 
    USERS.add(websocket)
    await notify_users()
    return

async def brightUnRegister(websocket):
    USERS.remove(websocket)
    for x in MAPPING_TOKEN_SOCKET:
        if MAPPING_TOKEN_SOCKET[x] == websocket:
            MAPPING_TOKEN_SOCKET.pop(x)
            break
    await notify_users()

async def notify_users():
    for user in USERS:
        '''
        if "umcsecrfslmlsnrnyqtxaivysyceaqkl" in MAPPING_TOKEN_SOCKET and user == MAPPING_TOKEN_SOCKET["umcsecrfslmlsnrnyqtxaivysyceaqkl"]:
            await asyncio.wait([user.send("hello " + str(user)) ])'''
        await asyncio.wait([user.send(json.dumps({'current_connected_users':len(MAPPING_TOKEN_SOCKET)}))])
    

async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    #await register(websocket)
    status = False;

    try:
        #await websocket.send(json.dumps({'no':len(MAPPING_TOKEN_SOCKET)}))
        mydb = mysql.connector.connect(
        host="quix.click",
        user="root",
        password="bobandyui.com",
        port="3306"
        )
        mycursor = mydb.cursor()
        async for message in websocket:
            message = json.loads(message)
            token = message['msg']['token_id']
            rid = message['rid']
            mycursor.execute("SELECT token FROM quixdt.TokenTable")
            list_of_tokens = mycursor.fetchall()
            for x in list_of_tokens:
                if x[0] == token:
                    await brightRegister(websocket,token)
                    status = True
                    print('login successfully')
                    result = success_authentication(rid,token)
                    print('1', result)
                    await websocket.send(result)
                    break
            if status == True:
                pass
            else:
                await websocket.send(fail_authentication(rid))
    finally:
        await brightUnRegister(websocket)

start_server = websockets.serve(counter, "localhost", 9999)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
