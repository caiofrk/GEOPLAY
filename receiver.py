import os
from fastapi import FastAPI, UploadFile, File
import uvicorn

# Configuration
UPLOAD_DIR = "uploads"
HOST = "0.0.0.0"  # Listen on all interfaces so the phone can connect
PORT = 8000

app = FastAPI()

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_scan(file: UploadFile = File(...)):
    """
    Endpoint to receive raw scan files (.obj, .ply, .mp4, etc.) from the Flutter app.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        # Read and write in chunks to handle massive scan files
        while chunk := await file.read(1024 * 1024):  # 1MB chunks
            buffer.write(chunk)
            
    print(f"[SUCCESS] Received and saved: {file_path}")
    
    # Here you could trigger the blender_pipeline.py automatically
    # e.g., os.system(f"blender --background --python blender_pipeline.py -- {file_path}")
    
    return {"status": "success", "filename": file.filename, "message": "File received and saved locally."}

if __name__ == "__main__":
    print(f"\nStarting Local Receiver Server on http://{HOST}:{PORT}")
    print(f"Make sure your phone is on the same Wi-Fi network and sends POST requests to http://<YOUR_PC_IP>:{PORT}/upload\n")
    uvicorn.run(app, host=HOST, port=PORT)
