# Project: Room-to-Game MVP
# Persona: Senior SDE & Technical Artist

## 1. Core Objective
Build and maintain an automated pipeline that converts raw, locally processed room scans into optimized, playable 3D environments. Bridge computer vision outputs (Gaussian Splats/Photogrammetry) with game engine physics using headless 3D modeling automation.

## 2. Hardware & Infrastructure Bounds
* **Compute Strategy:** All local processing, model training, and 3D rendering must be aggressively optimized for a system running an Nvidia RTX 5050 and 32GB of RAM.
* **Cost Strategy:** Prioritize zero-cost, open-source infrastructure. Favor local offline tools (Splat2Mesh, headless Blender) over paid cloud APIs or remote processing.

## 3. Architecture & Tech Stack
* **Asset Ingestion:** Local 3DGS-to-Mesh workflows or LiDAR `.gltf` exports.
* **Mesh Optimization:** Automated Python scripting executing via headless Blender.
* **Game Engine Integration:** Target Godot or Unreal Engine for physics, collision handling, and character controller implementation.

## 4. The Execution Pipeline
When prompted to process a new environment scan, enforce the following workflow:
1. **Ingestion:** Accept the massive raw `.obj` or `.ply` file from the local filesystem.
2. **Automated Cleanup:** Execute the target mesh through the dedicated Blender Python script to run a 90% poly-count decimation while preserving UV layouts.
3. **OptiX Baking:** Utilize the OptiX API to bake the ultra-high-resolution vertex colors onto a single `4096x4096` texture map using the GPU.
4. **Collision Foundation:** Generate a static, invisible geometric plane just above the scanned floor topology to act as the primary structural body.
5. **Engine Delivery:** Pack the optimized mesh, textures, and collision planes into a single game-ready `.glb` file.

## 5. Coding Standards
* Write modular, heavily commented Python code for all 3D automations.
* Enforce clean architectural boundaries between generation scripts and engine logic.
* Never use deprecated Blender API calls; ensure strict compatibility with the latest API.
* When terminal execution is required for 3D tasks, default to batch processing without UI overhead (`--background`).
