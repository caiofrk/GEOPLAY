# GeoPlay MVP: Progress & Roadmap

## Current Status
We are building the "Room-to-Game MVP" pipeline which converts raw, locally processed room scans into optimized, playable 3D environments.

### Completed Tasks
- [x] **Project Scaffolding**: Initialized git repo and linked to `https://github.com/caiofrk/GEOPLAY.git`.
- [x] **Architecture Rules**: Created `GEMINI.md` to dictate the local, zero-cost, RTX 5050-optimized pipeline rules.
- [x] **Blender Pipeline Script**: Created `blender_pipeline.py` to automate 90% poly-count decimation, UV generation, and OptiX baking.
- [x] **Capture App**: Built `room_scanner` Flutter app with a premium Dark Mode UI, camera recording, and real HTTP Multipart uploading.
- [x] **Local Server**: Built `receiver.py` (FastAPI) to handle incoming multi-part video/scan uploads in 1MB chunks to the local PC.
- [x] **Data Hygiene**: Added `.gitignore` to prevent raw captures in `uploads/` from bloating the repository.
- [x] **E2E Test**: Successfully recorded a mock video on Android and streamed it directly to the local PC `uploads/` folder.

### Pending Tasks (Next Steps)
- [ ] **Photogrammetry / Splatting Integration**: Feed the uploaded MP4/JPEG data into a local Gaussian Splat or Photogrammetry generator (e.g., COLMAP) to create the raw `.obj`.
- [ ] **Collision Generation**: Extend `blender_pipeline.py` to automatically detect the floor bounds and generate a static collision plane.
- [ ] **Game Engine Integration**: Import the baked `.glb` into Godot or Unreal Engine and set up a basic first-person character controller to walk around the room.
