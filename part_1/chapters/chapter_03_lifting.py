from manim import *
from core.base_scene import BaseChapter
from core.config import *

class Chapter03(BaseChapter):
    def construct(self):
        # ─────────────────────────────────────────────────────────
        # SCENE 3.1: THE CIRCULAR BUFFER
        # ─────────────────────────────────────────────────────────
        title = self.create_kinetic_title("[ THE MULTI-RESOLUTION ENGINE ]", color=COLOR_DIM_TEXT)
        title.to_corner(UL, buff=SAFE_MARGIN)
        self.safe_play(FadeIn(title))

        # Glowing Ring Buffer
        ring = Annulus(inner_radius=1.8, outer_radius=2.2, color=COLOR_GRID, fill_opacity=0.2)
        ring_glow = Annulus(inner_radius=1.7, outer_radius=2.3, color=COLOR_CYAN, fill_opacity=0.1)
        buffer_group = VGroup(ring_glow, ring).shift(UP*1)

        # Segments
        segments = VGroup()
        for i in range(16): # representing 128 visually
            angle = i * (2 * PI / 16)
            line = Line(
                start=ring.get_center() + np.array([1.8 * np.cos(angle), 1.8 * np.sin(angle), 0]),
                end=ring.get_center() + np.array([2.2 * np.cos(angle), 2.2 * np.sin(angle), 0]),
                color=COLOR_OBSIDIAN, stroke_width=4
            )
            segments.add(line)
        buffer_group.add(segments)

        self.safe_play(Create(buffer_group), run_time=1.5)

        # Data stream falling in
        stream_text = VGroup(*[Text(f"400.{i:02d}", font=FONT_MONO, font_size=16, color=COLOR_CYAN_BR) for i in range(10)])
        stream_text.arrange(DOWN, buff=0.2).next_to(buffer_group, UP, buff=2)
        
        self.play(stream_text.animate.next_to(buffer_group, UP, buff=0), run_time=1)
        self.play(FadeOut(stream_text, shift=DOWN), buffer_group.animate.rotate(PI/2), run_time=1)

        lbl_buffer = self.create_code_text("LOCK-FREE CIRCULAR BUFFER (128 SAMPLES)", color=WHITE).next_to(buffer_group, DOWN, buff=0.5)
        self.safe_play(Write(lbl_buffer))
        self.wait(1)

        # ─────────────────────────────────────────────────────────
        # SCENE 3.2: LAZY WAVELET SPLIT
        # ─────────────────────────────────────────────────────────
        self.safe_play(FadeOut(buffer_group), FadeOut(lbl_buffer))

        # Array of numbers
        data_array = VGroup(*[
            Text(f"x[{i}]", font=FONT_MONO, font_size=24, color=WHITE) for i in range(8)
        ]).arrange(DOWN, buff=0.3).to_edge(UP, buff=1.5)

        self.safe_play(FadeIn(data_array))

        # Prism
        prism = Triangle(color=COLOR_CYAN).scale(0.5).next_to(data_array, DOWN, buff=1)
        split_lbl = self.create_code_text("STEP 1: SPLIT (LAZY WAVELET)").next_to(prism, RIGHT, buff=0.5)
        
        self.safe_play(Create(prism), Write(split_lbl))

        # Split Even / Odd
        evens = VGroup(*[data_array[i] for i in range(0, 8, 2)])
        odds = VGroup(*[data_array[i] for i in range(1, 8, 2)])

        even_dest = VGroup(*[Text(f"x[{i}]", font=FONT_MONO, font_size=24, color=COLOR_CYAN) for i in range(0, 8, 2)]).arrange(DOWN, buff=0.3).move_to(LEFT * 3 + DOWN * 1)
        odd_dest = VGroup(*[Text(f"x[{i}]", font=FONT_MONO, font_size=24, color=COLOR_CRIMSON) for i in range(1, 8, 2)]).arrange(DOWN, buff=0.3).move_to(RIGHT * 3 + DOWN * 1)

        self.play(
            Transform(evens, even_dest),
            Transform(odds, odd_dest),
            run_time=1.5
        )

        lbl_even = Text("EVEN", font=FONT_SANS, font_size=20, color=COLOR_CYAN).next_to(evens, DOWN)
        lbl_odd = Text("ODD", font=FONT_SANS, font_size=20, color=COLOR_CRIMSON).next_to(odds, DOWN)
        self.safe_play(FadeIn(lbl_even), FadeIn(lbl_odd))

        # ─────────────────────────────────────────────────────────
        # SCENE 3.3: PREDICT AND UPDATE (THE LIFTING MATH)
        # ─────────────────────────────────────────────────────────
        self.safe_play(FadeOut(prism), FadeOut(split_lbl), FadeOut(data_array), FadeOut(title))

        # Lifting Blocks
        box_p = Rectangle(width=2, height=1, color=COLOR_CYAN, fill_opacity=0.2).move_to(UP * 1.5)
        lbl_p = Text("[ P ] PREDICT", font=FONT_MONO, font_size=18).move_to(box_p)
        
        box_u = Rectangle(width=2, height=1, color=COLOR_CYAN_BR, fill_opacity=0.2).move_to(DOWN * 1.5)
        lbl_u = Text("[ U ] UPDATE", font=FONT_MONO, font_size=18).move_to(box_u)

        boxes = VGroup(box_p, lbl_p, box_u, lbl_u)
        self.safe_play(FadeIn(boxes))

        # Adjust evens and odds layout for lasers
        self.play(evens.animate.move_to(LEFT*4), odds.animate.move_to(RIGHT*4))
        self.play(lbl_even.animate.next_to(evens, UP), lbl_odd.animate.next_to(odds, UP))

        # Laser Predict
        laser_p = Arrow(evens[0].get_right(), box_p.get_left(), color=COLOR_CYAN, buff=0.1)
        laser_p_out = Arrow(box_p.get_right(), odds[0].get_left(), color=COLOR_CRIMSON, buff=0.1)
        
        math_p = MathTex(r"d[n] = x_{odd}[n] - P(x_{even})", color=COLOR_CRIMSON, font_size=36).next_to(box_p, UP, buff=0.3)

        self.safe_play(GrowArrow(laser_p))
        self.safe_play(GrowArrow(laser_p_out), Write(math_p))
        
        # Turn odd into Detail
        d_text = Text("D1", font=FONT_MONO, font_size=24, color=COLOR_CRIMSON).move_to(odds[0])
        self.play(Transform(odds[0], d_text))

        # Laser Update
        laser_u = Arrow(odds[0].get_left(), box_u.get_right(), color=COLOR_CRIMSON, buff=0.1)
        laser_u_out = Arrow(box_u.get_left(), evens[0].get_right(), color=COLOR_CYAN_BR, buff=0.1)
        
        math_u = MathTex(r"a[n] = x_{even}[n] + U(d[n])", color=COLOR_CYAN_BR, font_size=36).next_to(box_u, DOWN, buff=0.3)

        self.safe_play(GrowArrow(laser_u))
        self.safe_play(GrowArrow(laser_u_out), Write(math_u))

        # Turn even into Approx
        a_text = Text("A1", font=FONT_MONO, font_size=24, color=COLOR_CYAN_BR).move_to(evens[0])
        self.play(Transform(evens[0], a_text))

        self.wait(1)

        # ─────────────────────────────────────────────────────────
        # SCENE 3.4: THE MRA CASCADE TREE
        # ─────────────────────────────────────────────────────────
        self.safe_play(
            FadeOut(boxes), FadeOut(laser_p), FadeOut(laser_p_out), 
            FadeOut(laser_u), FadeOut(laser_u_out), FadeOut(math_p), FadeOut(math_u),
            FadeOut(odds[1:]), FadeOut(evens[1:]), FadeOut(lbl_even), FadeOut(lbl_odd)
        )

        # Build a visual tree downward
        tree = VGroup()
        node_a1 = a_text.copy().move_to(UP*2)
        node_d1 = d_text.copy().move_to(UP*2 + RIGHT*4)
        tree.add(node_a1, node_d1, Line(UP*3, node_a1.get_top()), Line(UP*3, node_d1.get_top()))

        # Level 2
        node_a2 = Text("A2", font=FONT_MONO, font_size=24, color=COLOR_CYAN_BR).move_to(node_a1.get_center() + DOWN*1.5 + LEFT*1.5)
        node_d2 = Text("D2", font=FONT_MONO, font_size=24, color=COLOR_CRIMSON).move_to(node_a1.get_center() + DOWN*1.5 + RIGHT*1.5)
        tree.add(node_a2, node_d2, Line(node_a1.get_bottom(), node_a2.get_top()), Line(node_a1.get_bottom(), node_d2.get_top()))

        # Level 3
        node_a3 = Text("A3", font=FONT_MONO, font_size=24, color=COLOR_CYAN_BR).move_to(node_a2.get_center() + DOWN*1.5 + LEFT*1.5)
        node_d3 = Text("D3", font=FONT_MONO, font_size=24, color=COLOR_CRIMSON).move_to(node_a2.get_center() + DOWN*1.5 + RIGHT*1.5)
        tree.add(node_a3, node_d3, Line(node_a2.get_bottom(), node_a3.get_top()), Line(node_a2.get_bottom(), node_d3.get_top()))

        self.play(FadeOut(evens[0]), FadeOut(odds[0]))
        self.safe_play(Create(tree), run_time=2)

        # Final Tags
        tags = self.stack_vertical(
            self.create_kinetic_title("SWELDENS LIFTING SCHEME."),
            self.create_kinetic_title("MULTI-RESOLUTION ANALYSIS COMPLETE.", color=COLOR_CYAN_BR),
            buff=0.3, align_to=DOWN
        )
        self.safe_play(Write(tags))
        self.check_overlaps()
        self.wait(3)