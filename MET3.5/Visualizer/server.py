import asyncio
import websockets
import json
import sys
sys.path.append(r"C:\Users\jeffe\Desktop\Code Stuff\ETC\Cellular-Respiration-Sim\MET3.5")

from cytoplasm import cellState  
cell = cellState()

async def send_data(websocket):
    try:
        while True:
            cell.cycle()

            datasetCytoplasm = [cell.ADP, cell.ATP, cell.NAD, cell.NADH, cell.glucose, cell.pyruvate]
            keys = ["ADP", "ATP", "NAD", "NADH", "glucose", "pyruvate"]
            data_dict_cyto = dict(zip(keys, datasetCytoplasm))
            
            datasetMatrix = [cell.mitochondria.matrix.ADP, cell.mitochondria.matrix.ATP, cell.mitochondria.matrix.NAD, cell.mitochondria.matrix.NADH, cell.mitochondria.matrix.pyruvate, cell.mitochondria.matrix.GTP]
            keys = ["ADP", "ATP", "NAD", "NADH", "pyruvate", "GTP"]
            data_dict_matrix = dict(zip(keys, datasetMatrix))

            full_data = {
                "cytoplasm": data_dict_cyto,
                "matrix": data_dict_matrix
            }

            await websocket.send(json.dumps(full_data))
            await asyncio.sleep(0.5)

    except websockets.exceptions.ConnectionClosedOK:
        print("Client disconnected cleanly.")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Client disconnected with error: {e}")

async def main():
    print("WebSocket server starting on ws://localhost:6789")
    async with websockets.serve(send_data, "localhost", 6789):
        await asyncio.Future()  # run forever

asyncio.run(main())
