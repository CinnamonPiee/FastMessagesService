from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List


router = APIRouter()
active_connections: List[WebSocket] = []


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            for connection in active_connections:
                await connection.send_text(f"User {user_id}: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        await websocket.close()
