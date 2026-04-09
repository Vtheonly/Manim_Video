import subprocess
import os
import sys

# Define the exact 8 chapters and their file paths
CHAPTERS = [
    ("part_1/chapters/chapter_01_little_wave.py", "Chapter01"),
    ("part_1/chapters/chapter_02_biquads.py", "Chapter02"),
    ("part_1/chapters/chapter_03_lifting.py", "Chapter03"),
    ("part_1/chapters/chapter_04_discontinuity.py", "Chapter04"),
    ("part_1/chapters/chapter_05_esp32_edge.py", "Chapter05"),
    ("part_1/chapters/chapter_06_pybind11.py", "Chapter06"),
    ("part_1/chapters/chapter_07_precise_loc.py", "Chapter07"),
    ("part_1/chapters/chapter_08_consensus.py", "Chapter08"),
]

OUTPUT_DIR = "output_videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def render_chapter(filepath, classname):
    print(f"\n{'='*60}")
    print(f"🎬 RENDERING: {classname}")
    print(f"📁 PATH: {filepath}")
    print(f"{'='*60}")
    
    # Manim CLI flags:
    # --resolution 1280,720 : Strict 720p constraint
    # --frame_rate 50 : 50 FPS constraint for smooth scrolling
    # --media_dir : Route output safely into output_videos/
    
    cmd = [
        "manim",
        filepath,
        classname,
        "--resolution", "1280,720",
        "--frame_rate", "50",
        "--media_dir", OUTPUT_DIR,
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ SUCCESS: {classname} rendered successfully.")
    except subprocess.CalledProcessError:
        print(f"\n❌ ERROR: Failed to render {classname}.")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 INITIALIZING GPU RENDER PIPELINE...")
    
    for filepath, classname in CHAPTERS:
        if os.path.exists(filepath):
            render_chapter(filepath, classname)
        else:
            print(f"⚠️ SKIPPED: {filepath} does not exist yet.")
    
    print("\n🏁 ALL AVAILABLE CHAPTERS RENDERED. Check the 'output_videos/videos/' directory.")