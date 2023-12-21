import asyncio
import websockets
import os
from motor.motor_asyncio import AsyncIOMotorClient

from src.logs import Logger

async def chat_room(websocket, path):
    if len(connected) >= MAX_USERS:
        logger.warning("Server is full, rejecting connection.")
        await websocket.send("Server is full, try again later.")
        return
    connected.add(websocket)
    try:
        while True:
            message = await websocket.recv()
            logger.info(message)
            await db.messages.insert_one({'message': message})
            for conn in connected:
                logger.info(f"Sending message to {conn}")
                await conn.send(message)
    except websockets.exceptions.ConnectionClosed:
        logger.info("Connection closed")
        connected.remove(websocket)

async def main():
    async with websockets.serve(chat_room, "127.0.0.1", port):
        logger.info(f"Server started on port {port}")
        await asyncio.Future()

if __name__ == '__main__':
    logger = Logger("logs/bs_server.log")
    MAX_USERS = 10
    port = 13337
    client = AsyncIOMotorClient('mongodb://mongo')
    db = client.mydb
    if 'CHAT_PORT' in os.environ:
        port = int(os.environ['CHAT_PORT'])
    if 'MAX_USERS' in os.environ:
        MAX_USERS = int(os.environ['MAX_USERS'])
    connected = set()
    asyncio.run(main())