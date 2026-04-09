from manim import *
import numpy as np
from core.base_scene import BaseChapter
from core.config import *

class Chapter08(BaseChapter):
    def construct(self):
        # ─────────────────────────────────────────────────────────
        # SCENE 8.1: THE BOOLEAN VOTER
        # ─────────────────────────────────────────────────────────
        title = self.create_kinetic_title("[ CONSENSUS & SYSTEM ISOLATION ]", color=COLOR_DIM_TEXT)
        title.to_corner(UL, buff=SAFE_MARGIN)
        self.safe_play(FadeIn(title))

        # Logic Zones Setup
        zone_w, zone_h = 3.5, 2.5
        
        z1_box = Rectangle(width=zone_w, height=zone_h, color=COLOR_GRID, fill_opacity=0.2).move_to(LEFT * 4 + UP * 1)
        z1_title = self.create_code_text("ThresholdGuard", color=WHITE).scale(0.5).next_to(z1_box, UP, buff=0.1)
        z1_logic = MathTex(r"D1_{peak} > 100", font_size=28, color=COLOR_DIM_TEXT).move_to(z1_box)

        z2_box = Rectangle(width=zone_w, height=zone_h, color=COLOR_GRID, fill_opacity=0.2).move_to(RIGHT * 4 + UP * 1)
        z2_title = self.create_code_text("EnergyMonitor", color=WHITE).scale(0.5).next_to(z2_box, UP, buff=0.1)
        z2_logic = MathTex(r"D1_{energy} > 50", font_size=28, color=COLOR_DIM_TEXT).move_to(z2_box)

        # Center Voter Gate (OR Gate approximation)
        voter_box = Polygon(
            ORIGIN, RIGHT*1.5+UP*0.75, RIGHT*2.5, RIGHT*1.5+DOWN*0.75, ORIGIN+DOWN*1.5,
            color=COLOR_CYAN, fill_opacity=0.2
        ).move_to(UP * 1)
        voter_title = self.create_code_text("FaultVoter", color=COLOR_CYAN_BR).scale(0.5).next_to(voter_box, DOWN, buff=0.2)

        self.safe_play(
            Create(z1_box), Write(z1_title), Write(z1_logic),
            Create(z2_box), Write(z2_title), Write(z2_logic),
            Create(voter_box), Write(voter_title)
        )

        # Fault Trigger Simulation
        self.play(
            z1_box.animate.set_color(COLOR_CRIMSON).set_fill(opacity=0.4),
            z1_logic.animate.set_color(WHITE),
            z2_box.animate.set_color(COLOR_CRIMSON).set_fill(opacity=0.4),
            z2_logic.animate.set_color(WHITE),
            run_time=0.5
        )

        # Firing Lines into Voter
        l1 = Line(z1_box.get_right(), voter_box.get_left(), color=COLOR_CRIMSON, stroke_width=4)
        l2 = Line(z2_box.get_left(), voter_box.get_right(), color=COLOR_CRIMSON, stroke_width=4)

        self.safe_play(Create(l1), Create(l2), run_time=0.3)
        
        # Voter activates
        self.play(
            voter_box.animate.set_color(COLOR_CRIMSON).set_fill(opacity=0.8),
            run_time=0.2
        )

        consensus_text = self.create_kinetic_title("CONSENSUS REACHED. AVOIDING NUISANCE TRIP.", color=WHITE).scale(0.6)
        consensus_text.to_edge(DOWN, buff=SAFE_MARGIN)
        self.safe_play(Write(consensus_text))
        self.wait(1)

        # ─────────────────────────────────────────────────────────
        # SCENE 8.2: THE SNAPSHOT & ISOLATION
        # ─────────────────────────────────────────────────────────
        self.safe_play(
            FadeOut(z1_box), FadeOut(z1_title), FadeOut(z1_logic),
            FadeOut(z2_box), FadeOut(z2_title), FadeOut(z2_logic),
            FadeOut(voter_box), FadeOut(voter_title), FadeOut(l1), FadeOut(l2),
            FadeOut(consensus_text), FadeOut(title)
        )

        # The TripSequencer (Circuit Breaker)
        wire_left = Line(LEFT*5, LEFT*1.5, color=COLOR_CYAN, stroke_width=6)
        wire_right = Line(RIGHT*1.5, RIGHT*5, color=COLOR_CYAN, stroke_width=6)
        
        # The switch (Closed)
        switch = Line(LEFT*1.5, RIGHT*1.5, color=COLOR_CYAN, stroke_width=6)
        
        breaker_group = VGroup(wire_left, wire_right, switch).shift(UP * 2)
        cb_label = self.create_code_text("[ TripSequencer: RELAY CLOSED ]", color=COLOR_DIM_TEXT).scale(0.6).next_to(breaker_group, UP, buff=0.5)

        # The Data Stream (Below)
        stream_axes = Axes(
            x_range=[0, 10, 1], y_range=[-1, 1, 1],
            x_length=10, y_length=2,
            axis_config={"color": COLOR_GRID, "stroke_width": 1}
        ).shift(DOWN * 1.5)
        
        # Normal wave
        normal_wave = stream_axes.plot(lambda x: 0.5 * np.sin(5*x), color=COLOR_CYAN, stroke_width=2)
        
        self.safe_play(Create(breaker_group), Write(cb_label), Create(stream_axes), Create(normal_wave))

        # ACTION: SYSTEM TRIP
        # Switch snaps open
        trip_label = self.create_code_text("[ TripSequencer: RELAY OPEN ]", color=COLOR_CRIMSON).scale(0.6).move_to(cb_label)
        
        # Particle sparks
        sparks = VGroup(*[
            Dot(color=YELLOW, radius=0.05).move_to(LEFT*1.5)
            for _ in range(15)
        ])

        self.play(
            switch.animate.rotate(PI/4, about_point=LEFT*1.5).set_color(COLOR_DIM_TEXT),
            wire_left.animate.set_color(COLOR_DIM_TEXT),
            wire_right.animate.set_color(COLOR_DIM_TEXT),
            Transform(cb_label, trip_label),
            normal_wave.animate.set_color(COLOR_DIM_TEXT).apply_function(
                lambda p: [p[0], stream_axes.c2p(0,0)[1], p[2]] # Flatlines to 0
            ),
            run_time=0.2
        )
        
        # Scatter sparks
        self.play(
            sparks.animate.apply_function(
                lambda p: p + np.array([np.random.uniform(-1, 2), np.random.uniform(-1, 2), 0])
            ).set_opacity(0),
            run_time=0.5
        )

        # The Snapshot (ReplayRecorder)
        frame = Rectangle(width=10.5, height=2.5, color=YELLOW, stroke_width=2, stroke_dasharray=[0.2, 0.2]).move_to(stream_axes)
        frame_lbl = self.create_code_text("ReplayRecorder: Capturing pre-fault cache...", color=YELLOW).scale(0.5).next_to(frame, DOWN, buff=0.2)
        
        self.safe_play(Create(frame), Write(frame_lbl))
        self.wait(0.5)

        # Compress frame into JSON file
        json_file = VGroup(
            Rectangle(width=1.5, height=2, color=WHITE, fill_opacity=0.1),
            Polygon(UR*0.75+UP*0.25, UR*0.75+LEFT*0.25, UR*0.5, color=WHITE, fill_opacity=0.5), # Folded corner
            Text("JSON", font_size=16, color=YELLOW)
        ).move_to(stream_axes)

        json_lbl = self.create_code_text("trip_snapshot_20260207.json", color=WHITE).scale(0.5).next_to(json_file, DOWN, buff=0.2)

        self.play(
            ReplacementTransform(frame, json_file),
            ReplacementTransform(normal_wave, json_file),
            ReplacementTransform(stream_axes, json_file),
            ReplacementTransform(frame_lbl, json_lbl),
            run_time=1
        )
        self.wait(1)

        # Clean screen for final message
        self.safe_play(
            FadeOut(breaker_group), FadeOut(cb_label), 
            FadeOut(json_file), FadeOut(json_lbl)
        )

        # FINAL FRAME: Scanning line
        scan_line = Line(LEFT*7, RIGHT*7, color=COLOR_CYAN_BR, stroke_width=2).to_edge(UP)
        self.play(scan_line.animate.to_edge(DOWN), run_time=2, rate_func=linear)
        self.safe_play(FadeOut(scan_line))

        # Final Tag
        final_text = self.create_kinetic_title("PROTECTION AT THE SPEED OF MATH.", color=WHITE)
        self.safe_play(Write(final_text), run_time=2)
        
        # Subtle glow pulse on the final text
        self.play(Indicate(final_text, color=COLOR_CYAN_BR, scale_factor=1.05), run_time=2)
        
        self.check_overlaps()
        self.wait(3)