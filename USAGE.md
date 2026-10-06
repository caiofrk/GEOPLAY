# GeoPlay: Room-to-Game Pipeline

Welcome to GeoPlay! This project allows you to scan a physical room using your Android phone and automatically convert it into an optimized, playable 3D environment in Godot.

Here is the step-by-step guide to using the complete software pipeline.

---

## Step 1: Start the Local Receiver Server

First, you need to run the local server on your PC so it can receive video uploads from your phone over your local Wi-Fi.

1. Open a terminal in the `GEOPLAY` root directory.
2. Run the receiver script:
   ```bash
   python receiver.py
   ```
3. The console will print out the local IP address and port (usually `0.0.0.0:8000`). Find your PC's actual local IP address (e.g., `192.168.0.2`) if you need to configure the mobile app.

---

## Step 2: Record and Upload the Room Scan

Use the Android app to scan the room and send it to the PC.

1. Install and open the **GeoPlay Scanner** app on your Android device (ensure it's connected to the same Wi-Fi as your PC).
2. Tap the record button and slowly walk around the room, capturing all angles, surfaces, and the floor.
3. Tap the button again to stop recording.
4. When prompted, tap **Send to Local PC**. 
5. You should see a success message on your phone, and the `.mp4` file will appear in the `uploads/` folder on your PC.

*(Note: If the upload fails, ensure the IP address in `room_scanner/lib/main.dart` matches your PC's IP address and rebuild the app).*

---

## Step 3: 3D Reconstruction (Gaussian Splatting)

Convert the raw video scan into a 3D mesh.

1. Open a terminal in the `GEOPLAY` root directory.
2. Run the reconstruction pipeline on your uploaded video (replace the filename with your actual video):
   ```bash
   python reconstruction_pipeline.py --video uploads/REC123456789.mp4 --output processing_out
   ```
3. This script will orchestrate **Nerfstudio** to extract frames, run COLMAP, train a Gaussian Splat (`splatfacto`), and export it as a raw `.obj` mesh.
4. Once completed, the raw mesh will be saved at `processing_out/mesh.obj`.

---

## Step 4: Mesh Optimization & Collision Generation

The raw mesh is too heavy for a game engine, so we use headless Blender to optimize it, bake textures, and add an invisible collision floor.

1. Open `blender_pipeline.py` and ensure the `input_file` points to your newly generated mesh (e.g., `C:/path/to/GEOPLAY/processing_out/mesh.obj`) and `output_file` is set to where you want the final model (e.g., `godot_project/room.glb`).
2. Run the script via headless Blender from your terminal:
   ```bash
   blender --background --python blender_pipeline.py
   ```
3. Blender will automatically reduce the polycount by 90%, bake an optimized 4K OptiX texture, create a `Floor-colonly` collision plane, and export a game-ready `.glb` file!

---

## Step 5: Play in Godot

Walk around your newly scanned room!

1. Open the `godot_project/` folder using **Godot Engine 4.3+**.
2. If it isn't already there, drag and drop your optimized `room.glb` file into the `godot_project/` directory so Godot imports it.
3. Open `main.tscn`.
4. Drag your `room.glb` from the FileSystem dock directly into the scene hierarchy under the `RoomContainer` node.
5. Press the **Play** button (or `F5`).
6. Use **W, A, S, D** to move, **Space** to jump, and the mouse to look around your room!
