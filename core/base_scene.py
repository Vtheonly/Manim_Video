from manim import *
from core.config import *

class BaseChapter(Scene):
    """
    The master scene class. All chapters inherit from this.
    Enforces the Obsidian theme, kinetic typography, and safe-zone layouts.
    """

    def setup(self):
        """Forces the global background color before any rendering occurs."""
        self.camera.background_color = COLOR_OBSIDIAN
        
        # Frame boundaries for reference inside chapters
        self.safe_top    = SAFE_TOP
        self.safe_bottom = SAFE_BOTTOM
        self.safe_left   = SAFE_LEFT
        self.safe_right  = SAFE_RIGHT

    # ── KINETIC TYPOGRAPHY GENERATORS ────────────────────────────
    def create_kinetic_title(self, text: str, color=COLOR_TEXT):
        """Creates bold, heavy sans-serif text for kinetic impacts."""
        mob = Text(text, font=FONT_SANS, weight=BOLD, color=color, font_size=48)
        return fit_to_frame(mob)

    def create_code_text(self, text: str, color=COLOR_CYAN_BR):
        """Creates strict monospace text for math and code."""
        mob = Text(text, font=FONT_MONO, color=color, font_size=36)
        return fit_to_frame(mob)

    # ── SYSTEMATIC LAYOUT MANAGERS (ANTI-OVERLAP) ────────────────
    def safe_play(self, *animations, **kwargs):
        """Play animations, then strictly verify no objects overlap the edges."""
        self.play(*animations, **kwargs)
        for mob in self.mobjects:
            debug_frame_check(self, mob)

    def stack_vertical(self, *mobjects, buff=0.5, align_to=UP):
        """
        The ultimate fix for overlapping content.
        Pass in any number of objects, and they are automatically stacked,
        scaled to fit the frame, and aligned safely.
        """
        group = VGroup(*mobjects)
        group.arrange(DOWN, buff=buff)
        fit_to_frame(group)
        group.to_edge(align_to, buff=SAFE_MARGIN)
        return group

    def check_overlaps(self):
        """Terminal debug tool: Detects if any two objects on screen are touching."""
        mobs = self.mobjects
        for i, a in enumerate(mobs):
            for b in mobs[i+1:]:
                if self._do_overlap(a, b):
                    print(f"⚠️  CRITICAL OVERLAP DETECTED between {a} and {b}")

    def _do_overlap(self, a, b):
        """Simple bounding box collision detection."""
        return not (
            a.get_right()[0]  < b.get_left()[0]  or
            b.get_right()[0]  < a.get_left()[0]  or
            a.get_top()[1]    < b.get_bottom()[1] or
            b.get_top()[1]    < a.get_bottom()[1]
        )