# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import uvicorn
# import socketio

# # Initialize FastAPI and Socket.IO
# app = FastAPI()
# sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
# socket_app = socketio.ASGIApp(sio, static_files={'/': './'})

# # Add CORS middleware to allow cross-origin requests
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Mount Socket.IO ASGI app onto FastAPI app
# app.mount("/", socket_app)

# # In-memory storage for connected clients
# clients = []

# @sio.event
# async def connect(sid, environ):
#     clients.append(sid)
#     print(f"Client {sid} connected.")
#     await sio.emit('message', f"Client {sid} connected.", skip_sid=sid)

# @sio.event
# async def disconnect(sid):
#     clients.remove(sid)
#     print(f"Client {sid} disconnected.")
#     await sio.emit('message', f"Client {sid} disconnected.", skip_sid=sid)

# @sio.event
# async def message(sid, data):
#     print(f"Message from {sid}: {data}")
#     # Broadcast the message to all connected clients
#     await sio.emit('message', data, skip_sid=sid)

# @app.get("/api")
# def read_root():
#     return {"message": "Welcome to the real-time chat application!"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import socketio
import uvicorn

# Initialize FastAPI and Socket.IO
app = FastAPI()
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, static_files={'/': './static'})

# Serve the static directory where the HTML and font files are located
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount Socket.IO ASGI app onto FastAPI app
app.mount("/", socket_app)

# In-memory storage for connected clients
clients = []

@sio.event
async def connect(sid, environ):
    clients.append(sid)
    print(f"Client {sid} connected.")
    await sio.emit('message', f"Client {sid} connected.", skip_sid=sid)

@sio.event
async def disconnect(sid):
    clients.remove(sid)
    print(f"Client {sid} disconnected.")
    await sio.emit('message', f"Client {sid} disconnected.", skip_sid=sid)

@sio.event
async def message(sid, data):
    print(f"Message from {sid}: {data}")
    # Broadcast the message to all connected clients
    await sio.emit('message', data, skip_sid=sid)

@app.get("/")
def get():
    return FileResponse('static/index.html')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
