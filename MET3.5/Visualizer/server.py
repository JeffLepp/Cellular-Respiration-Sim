import asyncio
import websockets
import json
import sys
sys.path.append(r"C:\Users\jeffe\Desktop\Code Stuff\ETC\Cellular-Respiration-Sim\MET3.0")

from cytoplasm import cellState  
cell = cellState()

async def send_data(websocket, path):
    while True:
        cell.cycle()
        
        dataset = [cell.ADP, cell.ATP, cell.NAD, cell.NADH, cell.glucose, cell.pyruvate]
        keys = ["ADP", "ATP", "NAD", "NADH", "glucose", "pyruvate"]
        data_dict = dict(zip(keys, dataset))
        await websocket.send(json.dumps(data_dict))
        await asyncio.sleep(0.2)

start_server = websockets.serve(send_data, "localhost", 6789)
print("WebSocket server started on ws://localhost:6789")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
