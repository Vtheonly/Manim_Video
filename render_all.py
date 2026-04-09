# render_all.py
import subprocess
import os
import sys

CHAPTERS = [
    ("part_1/chapters/chapter_01_little_wave.py", "Chapter01"),
    ("part_1/chapters/chapter_02_biquads.py",     "Chapter02"),
    ("part_1/chapters/chapter_03_lifting.py",      "Chapter03"),
    ("part_1/chapters/chapter_04_discontinuity.py","Chapter04"),
    ("part_1/chapters/chapter_05_esp32_edge.py",   "Chapter05"),
    ("part_1/chapters/chapter_06_pybind11.py",     "Chapter06"),
    ("part_1/chapters/chapter_07_precise_loc.py",  "Chapter07"),
    ("part_1/chapters/chapter_08_consensus.py",    "Chapter08"),
]

OUTPUT_DIR = "output_videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# This is what was missing — subprocess needs to know where core/ is
env = os.environ.copy()
env["PYTHONPATH"] = os.getcwd()

def render_chapter(filepath, classname):
    print(f"\n{'='*60}")
    print(f"🎬 RENDERING: {classname}")
    print(f"📁 PATH: {filepath}")
    print(f"{'='*60}")

    cmd = [
        "manim",
        filepath,
        classname,
        "--resolution", "1280,720",
        "--frame_rate", "50",
        "--media_dir", OUTPUT_DIR,
    ]

    try:
        subprocess.run(cmd, check=True, env=env)
        print(f"\n✅ SUCCESS: {classname}")
    except subprocess.CalledProcessError:
        print(f"\n❌ ERROR: {classname} failed.")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 INITIALIZING GPU RENDER PIPELINE...")

    for filepath, classname in CHAPTERS:
        if os.path.exists(filepath):
            render_chapter(filepath, classname)
        else:
            print(f"⚠️  SKIPPED: {filepath} does not exist yet.")

    print("\n🏁 ALL AVAILABLE CHAPTERS RENDERED.")