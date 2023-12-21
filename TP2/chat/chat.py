import asyncio
import websockets
import redis.asyncio as aioredis
from motor.motor_asyncio import AsyncIOMotorClient
import os

from src.logs import Logger

global CLIENT, CONNECTIONS, MESSAGES, REDIS_CLIENT, DB, MAX_USERS
CONNECTIONS = {}
MESSAGES = []
# Create a new MongoDB client and get a reference to the mydb database
MONGO_CLIENT = AsyncIOMotorClient('mongodb://mongo')
DB = MONGO_CLIENT.mydb

async def chat_room(websocket, path):
    if len(CONNECTIONS) >= MAX_USERS:
        logger.warning("Server is full, rejecting connection.")
        await websocket.send("Server is full, try again later.")
        return
    await add_client(websocket, path)
    try:
        while True:
            message = await websocket.recv()
            await add_message(message)
            for conn in CONNECTIONS.values():
                await conn.send(message)
    except websockets.exceptions.ConnectionClosed:
        await remove_client(websocket)

async def add_client(websocket, path):
    formated_websocket = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    await REDIS_CLIENT.sadd('clients', formated_websocket)
    await DB.clients.insert_one({'client': formated_websocket})
    CONNECTIONS[formated_websocket] = websocket

async def add_message(message):
    await REDIS_CLIENT.sadd('messages', message)
    await DB.messages.insert_one({'message': message})

async def remove_client(websocket):
    formated_websocket = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    await REDIS_CLIENT.srem('clients', formated_websocket)
    await DB.clients.delete_one({'client': formated_websocket})
    del CONNECTIONS[formated_websocket]

async def main():
    async with websockets.serve(chat_room, "127.0.0.1", port):
        await asyncio.Future()

if __name__ == '__main__':
    logger = Logger("logs/bs_server.log")
    MAX_USERS = 10
    port = 13337
    if 'CHAT_PORT' in os.environ:
        port = int(os.environ['CHAT_PORT'])
    if 'MAX_USERS' in os.environ:
        MAX_USERS = int(os.environ['MAX_USERS'])
    CLIENT = aioredis.Redis(host='localhost', port=6379)
    asyncio.run(main())