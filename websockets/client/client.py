#!/usr/bin/env python

# WSS (WS over TLS) client example, with a self-signed certificate
import logging
import asyncio
import pathlib
import ssl
import websockets

logging.basicConfig(filename='example.log', level=logging.INFO)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("quix-client.pem")
ssl_context.load_verify_locations(localhost_pem)

async def hello():
    uri = "wss://th1.s.quix.click/oob/"
    async with websockets.connect(
        uri, ssl=True
    ) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())





