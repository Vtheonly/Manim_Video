from manim import *
import numpy as np
from core.base_scene import BaseChapter
from core.config import *

class Chapter07(BaseChapter):
    def construct(self):
        # ─────────────────────────────────────────────────────────
        # SCENE 7.1: TIME OF ARRIVAL (TOA)
        # ─────────────────────────────────────────────────────────
        title = self.create_kinetic_title("[ PRECISE FAULT LOCATION ]", color=COLOR_DIM_TEXT)
        title.to_corner(UL, buff=SAFE_MARGIN)
        self.safe_play(FadeIn(title))

        # D1 Coefficient Timeline
        axes = Axes(
            x_range=[0, 10, 1], y_range=[-1, 3, 1],
            x_length=10, y_length=3,
            axis_config={"color": COLOR_GRID, "stroke_width": 1}
        ).shift(UP * 1.5)

        # Generate a mostly flat D1 signal with a massive spike at x=6.5
        PEAK_X = 6.5
        def d1_signal(x):
            noise = np.random.normal(0, 0.05)
            spike = 2.5 * np.exp(-50 * (x - PEAK_X)**2) * np.cos(20 * (x - PEAK_X))
            return noise + spike

        # Pre-calculate to avoid jitter
        x_vals = np.linspace(0, 10, 500)
        y_vals = [d1_signal(x) for x in x_vals]
        
        d1_wave = axes.plot_line_graph(
            x_values=x_vals, y_values=y_vals,
            line_color=COLOR_CYAN, stroke_width=2, add_vertex_dots=False
        )

        self.safe_play(Create(axes), Create(d1_wave), run_time=2)

        # Crosshair Lock-on
        v_line = DashedLine(
            start=axes.c2p(PEAK_X, -1), end=axes.c2p(PEAK_X, 3), 
            color=COLOR_CRIMSON, stroke_width=3
        )
        h_line = DashedLine(
            start=axes.c2p(0, 2.5), end=axes.c2p(10, 2.5), 
            color=COLOR_CRIMSON, stroke_width=3
        )
        crosshair_dot = Dot(axes.c2p(PEAK_X, 2.5), color=WHITE, radius=0.1)
        
        # Lock on animation
        target_circle = Circle(radius=0.5, color=COLOR_CRIMSON).move_to(crosshair_dot)
        
        self.safe_play(
            Create(v_line), Create(h_line), FadeIn(crosshair_dot),
            Create(target_circle), run_time=1
        )
        self.play(target_circle.animate.scale(0.2).set_color(WHITE), run_time=0.5)

        # Data Overlays
        code_overlay = self.create_code_text("np.argmax(np.abs(d1_coeffs))", color=COLOR_CYAN_BR).scale(0.7)
        code_overlay.next_to(target_circle, UR, buff=0.2)
        
        toa_text = self.create_kinetic_title("1. TIME OF ARRIVAL (TOA) CAPTURED.", color=WHITE).scale(0.8)
        toa_text.to_edge(DOWN, buff=SAFE_MARGIN)

        self.safe_play(Write(code_overlay), FadeIn(toa_text, shift=UP))
        self.wait(1.5)

        # ─────────────────────────────────────────────────────────
        # SCENE 7.2: THE FREQUENCY DAMPING RATIO
        # ─────────────────────────────────────────────────────────
        self.safe_play(
            FadeOut(axes), FadeOut(d1_wave), FadeOut(v_line), FadeOut(h_line),
            FadeOut(crosshair_dot), FadeOut(target_circle), FadeOut(code_overlay),
            FadeOut(toa_text)
        )

        # Spheres of Energy
        d1_tracker = ValueTracker(3.0) # Represents radius/energy
        d2_tracker = ValueTracker(1.0)

        # High Freq Sphere (D1)
        d1_sphere = always_redraw(lambda: VGroup(
            Circle(radius=d1_tracker.get_value(), color=COLOR_CRIMSON, fill_opacity=0.3, stroke_width=0),
            Circle(radius=d1_tracker.get_value()*0.9, color=COLOR_CRIMSON, fill_opacity=0.6, stroke_width=2)
        ).move_to(LEFT * 3 + UP * 1))
        d1_label = self.create_code_text("D1 ENERGY\n(High Freq)", color=COLOR_CRIMSON).scale(0.6).next_to(d1_sphere, UP, buff=0.5)

        # Mid Freq Sphere (D2)
        d2_sphere = always_redraw(lambda: VGroup(
            Circle(radius=d2_tracker.get_value(), color=COLOR_CYAN_BR, fill_opacity=0.3, stroke_width=0),
            Circle(radius=d2_tracker.get_value()*0.9, color=COLOR_CYAN_BR, fill_opacity=0.6, stroke_width=2)
        ).move_to(RIGHT * 3 + UP * 1))
        d2_label = self.create_code_text("D2 ENERGY\n(Mid Freq)", color=COLOR_CYAN_BR).scale(0.6).next_to(d2_sphere, UP, buff=0.5)

        self.safe_play(FadeIn(d1_sphere), FadeIn(d1_label), FadeIn(d2_sphere), FadeIn(d2_label))

        # The Math Ratio
        ratio_equation = MathTex(r"\text{Ratio} = \frac{D1}{D2}", font_size=48, color=WHITE).move_to(UP*1)
        self.safe_play(Write(ratio_equation))

        # Dynamic Number displays
        ratio_val = always_redraw(lambda: DecimalNumber(
            d1_tracker.get_value() / d2_tracker.get_value(),
            num_decimal_places=2, color=WHITE, font_size=48
        ).next_to(ratio_equation, DOWN, buff=0.5))

        self.safe_play(FadeIn(ratio_val))

        # Scenario A: Close Fault (D1 Massive)
        scen_a_text = self.create_kinetic_title("HIGH D1 = SHARP TRANSIENT = CLOSE FAULT (50m)", color=COLOR_CRIMSON).scale(0.6)
        scen_a_text.to_edge(DOWN, buff=SAFE_MARGIN)
        self.safe_play(Write(scen_a_text))
        self.wait(1)

        # Scenario B: Far Fault (D1 Attenuated over distance)
        self.safe_play(FadeOut(scen_a_text))
        
        scen_b_text = self.create_kinetic_title("LOW D1 = ATTENUATED TRANSIENT = DISTANT FAULT (500m)", color=COLOR_CYAN_BR).scale(0.6)
        scen_b_text.to_edge(DOWN, buff=SAFE_MARGIN)
        
        self.play(
            d1_tracker.animate.set_value(0.99), # D1 shrinks massively due to cable attenuation
            FadeIn(scen_b_text),
            run_time=2, rate_func=ease_in_out_sine
        )
        self.wait(1)

        # The Final Equation
        self.safe_play(
            FadeOut(d1_sphere), FadeOut(d1_label), FadeOut(d2_sphere), FadeOut(d2_label),
            FadeOut(ratio_equation), FadeOut(ratio_val), FadeOut(title)
        )

        final_eq = MathTex(r"\text{Distance}_{m} = \frac{500}{\text{Ratio} + 0.01}", font_size=60, color=YELLOW)
        final_eq.move_to(UP * 1)
        
        self.safe_play(Write(final_eq), run_time=1.5)

        tags = self.stack_vertical(
            self.create_kinetic_title("PRECISE DISTANCE MAPPED", color=WHITE),
            self.create_kinetic_title("WITHOUT EXTRA SENSORS.", color=COLOR_CYAN_BR),
            buff=0.3, align_to=DOWN
        )
        
        self.safe_play(FadeOut(scen_b_text), Write(tags))
        self.check_overlaps()
        self.wait(3)