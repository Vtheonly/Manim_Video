from manim import *
from core.base_scene import BaseChapter
from core.config import *

class Chapter06(BaseChapter):
    def construct(self):
        # ─────────────────────────────────────────────────────────
        # SCENE 6.1: THE PYTHON GIL BOTTLENECK
        # ─────────────────────────────────────────────────────────
        title = self.create_kinetic_title("[ HYPER-PERFORMANCE ARCHITECTURE ]", color=COLOR_DIM_TEXT)
        title.to_corner(UL, buff=SAFE_MARGIN)
        self.safe_play(FadeIn(title))

        # The GIL Wall
        gil_wall = Rectangle(width=1.5, height=5, color=COLOR_CRIMSON, fill_opacity=0.3, stroke_width=4)
        gil_wall.move_to(ORIGIN)
        gil_text = Text("PYTHON\nGIL\nLOCK", font=FONT_SANS, font_size=24, color=COLOR_CRIMSON).move_to(gil_wall)
        
        self.safe_play(FadeIn(gil_wall), Write(gil_text))

        # Data arriving (Fast -> Slow)
        left_src = LEFT * 6
        right_dst = RIGHT * 6

        packet1 = Dot(color=COLOR_CYAN_BR, radius=0.15).move_to(left_src + UP*1)
        packet2 = Dot(color=COLOR_CYAN_BR, radius=0.15).move_to(left_src + DOWN*1)

        # Packets hit the wall and crawl
        self.play(
            packet1.animate.move_to(gil_wall.get_left() + UP*1),
            packet2.animate.move_to(gil_wall.get_left() + DOWN*1),
            run_time=0.5, rate_func=linear
        )
        
        padlock = Text("🔒", font_size=36).next_to(gil_wall, UP)
        self.safe_play(FadeIn(padlock, shift=DOWN))

        self.play(
            packet1.animate.move_to(gil_wall.get_right() + UP*1),
            packet2.animate.move_to(gil_wall.get_right() + DOWN*1),
            run_time=3, rate_func=linear # Very slow
        )

        warn_text = self.create_kinetic_title("PYTHON IS TOO SLOW FOR MICROSECOND FAULTS.", color=COLOR_CRIMSON).scale(0.7)
        warn_text.to_edge(DOWN, buff=SAFE_MARGIN)
        self.safe_play(Write(warn_text))
        self.wait(1)

        # ─────────────────────────────────────────────────────────
        # SCENE 6.2: THE ZERO-COPY MEMORY BRIDGE
        # ─────────────────────────────────────────────────────────
        self.safe_play(FadeOut(packet1), FadeOut(packet2), FadeOut(padlock), FadeOut(warn_text))

        # The Golden Tunnel (PyBind11 Bridge)
        tunnel = Rectangle(width=6, height=1.2, color=YELLOW, fill_opacity=0.2, stroke_width=4)
        tunnel.move_to(DOWN * 1.5)
        
        tunnel_lbl = self.create_code_text("[ PYBIND11 C++ NATIVE BRIDGE ]", color=YELLOW).scale(0.6)
        tunnel_lbl.next_to(tunnel, DOWN, buff=0.2)

        self.safe_play(Create(tunnel), FadeIn(tunnel_lbl))

        # The Zero-Copy Heuristic (Pointer Swapping)
        py_buffer = VGroup(
            Rectangle(width=2, height=1, color=COLOR_GRID, fill_opacity=0.8),
            Text("Python Numpy", font_size=16)
        ).move_to(LEFT * 4 + DOWN * 1.5)

        cpp_buffer = VGroup(
            Rectangle(width=2, height=1, color=COLOR_CYAN, fill_opacity=0.2),
            Text("C++ std::vector", font_size=16)
        ).move_to(RIGHT * 4 + DOWN * 1.5)

        self.safe_play(FadeIn(py_buffer), FadeIn(cpp_buffer))

        # Hex Addresses
        hex_py = Text("0x7FFF5FBFF", font=FONT_MONO, font_size=16, color=YELLOW).next_to(py_buffer, UP, buff=0.2)
        hex_cpp = Text("0x000000000", font=FONT_MONO, font_size=16, color=COLOR_DIM_TEXT).next_to(cpp_buffer, UP, buff=0.2)

        self.safe_play(FadeIn(hex_py), FadeIn(hex_cpp))

        # The actual zero-copy shift: The labels swap, data doesn't move
        self.play(
            Swap(hex_py, hex_cpp),
            run_time=1, rate_func=ease_in_out_sine
        )
        
        self.play(Indicate(hex_py, color=COLOR_CYAN_BR), Indicate(cpp_buffer, color=COLOR_CYAN_BR))

        zero_copy_lbl = self.create_kinetic_title("ZERO-COPY MEMORY SHIFT. NO DATA DUPLICATION.", color=WHITE).scale(0.6)
        zero_copy_lbl.to_edge(DOWN, buff=SAFE_MARGIN)
        self.safe_play(Write(zero_copy_lbl))
        self.wait(1.5)

        # ─────────────────────────────────────────────────────────
        # SCENE 6.3: THE MICROSECOND STOPWATCH
        # ─────────────────────────────────────────────────────────
        self.safe_play(
            FadeOut(gil_wall), FadeOut(gil_text), FadeOut(tunnel), FadeOut(tunnel_lbl),
            FadeOut(py_buffer), FadeOut(cpp_buffer), FadeOut(hex_py), FadeOut(hex_cpp),
            FadeOut(zero_copy_lbl), FadeOut(title)
        )

        # Stopwatch Breakdown
        header = self.create_kinetic_title("THE C++ FAST PATH TIMELINE", color=COLOR_CYAN_BR)
        header.to_edge(UP, buff=SAFE_MARGIN)
        self.safe_play(FadeIn(header))

        timeline_group = VGroup()
        
        steps = [
            ("00 µs", "ADC SAMPLE ACQUIRED"),
            ("05 µs", "POINTER SHIFT (PYBIND11)"),
            ("18 µs", "DWT LIFTING SCHEME EXECUTED"),
            ("35 µs", "FAULT DETECTED & TRIP FIRED")
        ]

        for time_str, desc in steps:
            t_mob = Text(time_str, font=FONT_MONO, font_size=32, color=YELLOW)
            d_mob = Text(desc, font=FONT_SANS, font_size=28, color=WHITE)
            row = VGroup(t_mob, d_mob).arrange(RIGHT, buff=0.5)
            timeline_group.add(row)

        timeline_group.arrange(DOWN, buff=0.8, aligned_edge=LEFT).move_to(ORIGIN)

        for row in timeline_group:
            self.safe_play(FadeIn(row[0], shift=RIGHT*0.5), Write(row[1]), run_time=0.7)
            self.wait(0.2)

        # Final Comparison Tag
        tags = self.stack_vertical(
            self.create_kinetic_title("TOTAL EXECUTION: 35 MICROSECONDS."),
            self.create_code_text("A mechanical breaker takes 50,000µs to open. The math is already waiting.", color=COLOR_DIM_TEXT).scale(0.6),
            buff=0.3, align_to=DOWN
        )

        self.safe_play(Write(tags))
        self.check_overlaps()
        self.wait(3)