import asyncio
import websockets
import datetime

connected_clients = set()
chat_history = []
MAX_CHAT_HISTORY = 10


async def handle_message(message, client, username):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"{timestamp} - {username}: {message}"
    print(f"{timestamp} Received message from {username}: {message}")

    chat_history.append(formatted_message)
    if len(chat_history) > MAX_CHAT_HISTORY:
        chat_history.pop(0)

    for c in connected_clients:
        if c != client:
            await c.send(formatted_message)


async def register(websocket):
    connected_clients.add(websocket)
    print(f"New client connected: {websocket.remote_address}")


async def unregister(websocket):
    connected_clients.remove(websocket)
    print(f"Client disconnected: {websocket.remote_address}")


async def server(websocket,path):
    await register(websocket)
    try:
        username = await websocket.recv()
        print(f"Username received from {websocket.remote_address}: {username}")

        for message in chat_history:
            await websocket.send(message)

        while True:
            message = await websocket.recv()
            await handle_message(message, websocket, username)
    except websockets.exceptions.ConnectionClosedError:
        pass
    finally:
        await unregister(websocket)


start_server = websockets.serve(server, "localhost", 8765)

print("Chat server started. Listening on ws://localhost:8765")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

