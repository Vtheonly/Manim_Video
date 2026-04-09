from manim import *

# ── STRICT VISUAL LANGUAGE (PALETTE) ─────────────────────────────
COLOR_OBSIDIAN = "#0B0C10"
COLOR_GRID     = "#1F2833"
COLOR_CYAN     = "#45A29E"
COLOR_CYAN_BR  = "#66FCF1"
COLOR_CRIMSON  = "#ED254E"
COLOR_TEXT     = "#FFFFFF"
COLOR_DIM_TEXT = "#8892B0"

# Font configurations
FONT_MONO      = "JetBrains Mono" # Fallback to standard monospace if missing
FONT_SANS      = "Helvetica Neue" # Fallback to standard sans-serif if missing

# ── SAFE ZONE CONSTANTS (FOR 720p RESOLUTION) ────────────────────
FRAME_W = config.frame_width
FRAME_H = config.frame_height

SAFE_MARGIN = 0.4
SAFE_LEFT   = -FRAME_W/2 + SAFE_MARGIN
SAFE_RIGHT  =  FRAME_W/2 - SAFE_MARGIN
SAFE_TOP    =  FRAME_H/2 - SAFE_MARGIN
SAFE_BOTTOM = -FRAME_H/2 + SAFE_MARGIN

# ── BOUNDARY MATHEMATICS ─────────────────────────────────────────
def is_in_frame(mobject, margin=SAFE_MARGIN):
    """Check if mobject is fully within frame boundaries."""
    left = mobject.get_left()[0]
    right = mobject.get_right()[0]
    top = mobject.get_top()[1]
    bottom = mobject.get_bottom()[1]

    return (
        left >= SAFE_LEFT and
        right <= SAFE_RIGHT and
        top <= SAFE_TOP and
        bottom >= SAFE_BOTTOM
    )

def fit_to_frame(mobject, margin=SAFE_MARGIN):
    """Automatically scale object down if it breaches the frame."""
    max_w = FRAME_W - margin * 2
    max_h = FRAME_H - margin * 2

    if mobject.width > max_w:
        mobject.scale_to_fit_width(max_w)

    if mobject.height > max_h:
        mobject.scale_to_fit_height(max_h)

    return mobject

def debug_frame_check(scene, *mobjects):
    """Print terminal warnings if any mobject clips outside the safe zone."""
    for mob in mobjects:
        if not is_in_frame(mob):
            print(f"⚠️  WARNING: {mob} is OUT OF FRAME")
            print(f"   Position : {mob.get_center()}")
            print(f"   Width    : {mob.width:.2f} / Max {FRAME_W:.2f}")
            print(f"   Height   : {mob.height:.2f} / Max {FRAME_H:.2f}")