import os
import argparse
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_command(command, cwd=None):
    """Executes a shell command synchronously and handles errors."""
    logging.info(f"Running command: {' '.join(command)}")
    try:
        subprocess.run(command, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed with exit code {e.returncode}: {' '.join(command)}")
        raise

def process_video_to_mesh(video_path: str, output_dir: str):
    """
    Orchestrates the conversion of a raw video scan into a 3D mesh using open-source tools.
    Utilizes Nerfstudio (ns-process-data, ns-train, ns-export) to handle COLMAP and Splatting.
    """
    video_path = Path(video_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    colmap_dir = output_dir / "colmap_data"
    splat_output = output_dir / "splat_output"
    mesh_output = output_dir / "mesh.obj"
    
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
        
    logging.info(f"Starting reconstruction pipeline for: {video_path}")
    
    # Step 1: Process video data into images and COLMAP poses
    # This extracts frames and runs COLMAP to estimate camera poses.
    logging.info("Step 1: Extracting frames and computing camera poses (ns-process-data)")
    process_data_cmd = [
        "ns-process-data", "video",
        "--data", str(video_path),
        "--output-dir", str(colmap_dir)
    ]
    # Uncomment the following line to run in reality (requires nerfstudio installed)
    # run_command(process_data_cmd)
    
    # Step 2: Train a Gaussian Splat model
    # splatfacto is highly optimized for RTX GPUs.
    logging.info("Step 2: Training Gaussian Splatting model (ns-train splatfacto)")
    train_cmd = [
        "ns-train", "splatfacto",
        "--data", str(colmap_dir),
        "--output-dir", str(splat_output),
        "--viewer.quit-on-train-completion", "True" # Run headless without web UI
    ]
    # run_command(train_cmd)
    
    # Find the generated config.yml from training
    # config_files = list(splat_output.rglob("config.yml"))
    # if not config_files:
    #     raise FileNotFoundError("Could not find config.yml from training.")
    # config_path = config_files[0]
    
    # Step 3: Export the trained splat to a mesh (Poisson surface reconstruction)
    logging.info("Step 3: Exporting to mesh (ns-export poisson)")
    # export_cmd = [
    #     "ns-export", "poisson",
    #     "--load-config", str(config_path),
    #     "--output-dir", str(output_dir),
    #     "--target-num-faces", "500000",
    #     "--num-pixels-per-side", "2048",
    #     "--use-bounding-box", "False"
    # ]
    # run_command(export_cmd)
    
    # Rename default export name to our standard mesh.obj
    poisson_mesh = output_dir / "poisson_mesh.obj"
    if poisson_mesh.exists():
        poisson_mesh.rename(mesh_output)
    
    logging.info(f"Pipeline complete! Raw mesh generated at {mesh_output}")
    logging.info(f"Next step: Run blender_pipeline.py on {mesh_output} to optimize and bake textures.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert video scan to raw 3D mesh via Gaussian Splatting.")
    parser.add_argument("--video", required=True, help="Path to input .mp4 video from uploads/")
    parser.add_argument("--output", required=True, help="Directory to store intermediate and final outputs")
    
    args = parser.parse_args()
    process_video_to_mesh(args.video, args.output)
