import asyncio
import websockets
import datetime


async def handle_message(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - {message}")


async def chat_client():
    username = input("Enter your username: ")
    async with websockets.connect("ws://localhost:8765") as websocket:
        print("Connected to the chat server.")
        await websocket.send(username)

        try:
            while True:
                message = input("You: ")
                await websocket.send(message)
        except websockets.exceptions.ConnectionClosedError:
            print("Connection to server closed.")


asyncio.get_event_loop().run_until_complete(chat_client())

