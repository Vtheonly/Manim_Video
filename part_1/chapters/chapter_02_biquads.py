from manim import *
import numpy as np
from core.base_scene import BaseChapter
from core.config import *

class Chapter02(BaseChapter):
    def construct(self):
        # ─────────────────────────────────────────────────────────
        # SCENE 2.1: THE THREAT OF ALIASING
        # ─────────────────────────────────────────────────────────
        title = self.create_kinetic_title("[ SIGNAL CONDITIONING ]", color=COLOR_DIM_TEXT)
        title.to_corner(UL, buff=SAFE_MARGIN)
        self.safe_play(FadeIn(title))

        axes = Axes(
            x_range=[0, 10, 1], y_range=[-3, 3, 1],
            x_length=12, y_length=4,
            axis_config={"color": COLOR_GRID}
        ).shift(UP * 0.5)

        # Chaotic signal: 50Hz base + extreme high freq noise
        def chaotic_signal(x, t):
            base = np.sin(2 * x - t)
            noise = 0.5 * np.sin(30 * x - 5 * t) + 0.3 * np.cos(45 * x - 7 * t)
            return base + noise

        time_tracker = ValueTracker(0)
        
        chaotic_wave = always_redraw(
            lambda: axes.plot(lambda x: chaotic_signal(x, time_tracker.get_value()), color=COLOR_CRIMSON, stroke_width=2)
        )

        self.safe_play(Create(axes), FadeIn(chaotic_wave))
        self.play(time_tracker.animate.increment_value(3), run_time=2, rate_func=linear)

        # The Nyquist Mirror
        nyquist_limit = self.create_code_text("[ NYQUIST LIMIT: 10 kHz ]", color=COLOR_CRIMSON)
        nyquist_limit.next_to(axes, DOWN, buff=0.5)
        
        mirror_line = DashedLine(
            start=axes.c2p(5, -3), end=axes.c2p(5, 3), 
            color=COLOR_CRIMSON, stroke_width=4
        )

        self.safe_play(FadeIn(nyquist_limit), Create(mirror_line))
        
        alias_warn = self.create_kinetic_title("UNFILTERED NOISE DESTROYS WAVELET ACCURACY.", color=WHITE)
        alias_warn.scale(0.8).to_edge(DOWN, buff=SAFE_MARGIN)
        self.safe_play(Write(alias_warn))
        self.wait(1.5)

        # ─────────────────────────────────────────────────────────
        # SCENE 2.2: THE 4TH-ORDER BUTTERWORTH FILTER
        # ─────────────────────────────────────────────────────────
        self.safe_play(
            FadeOut(chaotic_wave), FadeOut(mirror_line), FadeOut(axes), 
            FadeOut(nyquist_limit), FadeOut(alias_warn), FadeOut(title)
        )

        # Biquad Geometry Build
        biquad_1 = self._build_biquad_schematic("BIQUAD 1 (Q=0.54)").shift(LEFT * 3.5)
        biquad_2 = self._build_biquad_schematic("BIQUAD 2 (Q=1.30)").shift(RIGHT * 3.5)
        
        connection = Arrow(biquad_1.get_right(), biquad_2.get_left(), color=COLOR_CYAN, buff=0.2)
        
        system = VGroup(biquad_1, connection, biquad_2)
        fit_to_frame(system)
        system.shift(UP * 1)

        self.safe_play(DrawBorderThenFill(biquad_1), run_time=1.5)
        self.safe_play(GrowArrow(connection), DrawBorderThenFill(biquad_2), run_time=1.5)

        # Filtering Animation
        raw_label = self.create_code_text("RAW + NOISE", color=COLOR_CRIMSON).scale(0.6).next_to(biquad_1, LEFT, buff=0.5)
        clean_label = self.create_code_text("CLEANED (DELAYED)", color=COLOR_CYAN_BR).scale(0.6).next_to(biquad_2, RIGHT, buff=0.5)

        # Visualizing data flow through the blocks
        data_particle = Dot(color=COLOR_CRIMSON, radius=0.1).move_to(raw_label)
        self.safe_play(FadeIn(raw_label), FadeIn(clean_label), FadeIn(data_particle))

        # Path through blocks
        path_p1 = Line(raw_label.get_right(), biquad_1.get_left())
        path_p2 = Line(biquad_1.get_right(), biquad_2.get_left())
        path_p3 = Line(biquad_2.get_right(), clean_label.get_left())

        self.play(MoveAlongPath(data_particle, path_p1), run_time=0.5)
        self.play(data_particle.animate.set_color(YELLOW)) # Partially filtered
        self.play(MoveAlongPath(data_particle, path_p2), run_time=0.5)
        self.play(data_particle.animate.set_color(COLOR_CYAN_BR)) # Fully filtered
        self.play(MoveAlongPath(data_particle, path_p3), run_time=0.5)
        self.safe_play(FadeOut(data_particle))

        # Final Tags
        tags = self.stack_vertical(
            self.create_kinetic_title("4TH-ORDER IIR FILTER."),
            self.create_kinetic_title("ANTI-ALIASING ENGAGED.", color=COLOR_CYAN_BR),
            buff=0.3, align_to=DOWN
        )
        self.safe_play(Write(tags))
        self.check_overlaps()
        self.wait(3)

    def _build_biquad_schematic(self, label_text):
        """Generates a massive, detailed Direct-Form II Biquad diagram."""
        box = RoundedRectangle(width=5, height=4, color=COLOR_GRID, fill_opacity=0.8, fill_color=COLOR_OBSIDIAN)
        label = Text(label_text, font=FONT_MONO, font_size=20, color=WHITE).next_to(box.get_top(), DOWN, buff=0.2)
        
        # Internal nodes (Summers & Delays)
        sum1 = Circle(radius=0.2, color=COLOR_CYAN).move_to(box.get_center() + LEFT*1.5 + UP*0.5)
        sum1_plus = Text("+", font_size=16).move_to(sum1)
        
        z1 = Square(side_length=0.5, color=COLOR_DIM_TEXT).move_to(box.get_center() + DOWN*0.5)
        z1_label = Text("Z⁻¹", font_size=16).move_to(z1)
        
        z2 = Square(side_length=0.5, color=COLOR_DIM_TEXT).move_to(box.get_center() + DOWN*1.5)
        z2_label = Text("Z⁻¹", font_size=16).move_to(z2)

        sum2 = Circle(radius=0.2, color=COLOR_CYAN).move_to(box.get_center() + RIGHT*1.5 + UP*0.5)
        sum2_plus = Text("+", font_size=16).move_to(sum2)

        # Multiplier triangles
        def make_gain(text, pos):
            tri = Triangle(color=COLOR_CRIMSON).scale(0.15).move_to(pos).rotate(-PI/2)
            lbl = Text(text, font_size=12, color=WHITE).next_to(tri, UP, buff=0.1)
            return VGroup(tri, lbl)

        b0 = make_gain("b0", box.get_center() + RIGHT*0.75 + UP*0.5)
        b1 = make_gain("b1", box.get_center() + RIGHT*0.75 + DOWN*0.5)
        a1 = make_gain("-a1", box.get_center() + LEFT*0.75 + DOWN*0.5).rotate(PI) # Feedback
        
        # Lines (just structural representation, not fully wired to save render compute)
        wire_color = COLOR_DIM_TEXT
        l1 = Line(box.get_left(), sum1.get_left(), color=wire_color)
        l2 = Line(sum1.get_right(), sum2.get_left(), color=wire_color)
        l3 = Line(sum2.get_right(), box.get_right(), color=wire_color)
        
        return VGroup(box, label, sum1, sum1_plus, z1, z1_label, z2, z2_label, sum2, sum2_plus, b0, b1, a1, l1, l2, l3)