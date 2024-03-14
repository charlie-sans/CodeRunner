import asyncio
import websockets
import pexpect
import os

WS_HOST = "127.0.0.1"
WS_PORT = 5000

TEMP_PYTHON_FILE = "temp.py"

async def execute_code(code, websocket):
    with open(TEMP_PYTHON_FILE, 'w') as file:
        file.write(code)
    
    child = pexpect.spawn(f"python3 {TEMP_PYTHON_FILE}", encoding="utf-8")

    while True:
        try:
            index = child.expect(['\n', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
            if index == 0:
                await websocket.send(child.before)
            elif index == 1:
                await websocket.send(child.before)
                break
        except pexpect.exceptions.TIMEOUT:
            break
    os.remove(TEMP_PYTHON_FILE)

async def server(websocket, path):
    try:
        async for code in websocket:
            await execute_code(code, websocket)
    except websockets.exceptions.ConnectionClosedOK:
        pass


ws_server = websockets.serve(server, WS_HOST, WS_PORT)

asyncio.get_event_loop().run_until_complete(ws_server)
asyncio.get_event_loop().run_forever()