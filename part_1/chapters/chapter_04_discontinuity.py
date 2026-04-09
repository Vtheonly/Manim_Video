from manim import *
import numpy as np
from core.base_scene import BaseChapter
from core.config import *

class Chapter04(BaseChapter):
    def construct(self):
        # ─────────────────────────────────────────────────────────
        # SCENE 4.1: THE SLIDING WINDOW
        # ─────────────────────────────────────────────────────────
        title = self.create_kinetic_title("[ THE DISCONTINUITY HUNTER ]", color=COLOR_DIM_TEXT)
        title.to_corner(UL, buff=SAFE_MARGIN)
        self.safe_play(FadeIn(title))

        # Setup Axes
        axes = Axes(
            x_range=[0, 20, 2], y_range=[-3, 3, 1],
            x_length=12, y_length=4,
            axis_config={"color": COLOR_GRID, "stroke_width": 1}
        ).shift(UP * 0.5)
        self.safe_play(Create(axes), run_time=1)

        # 400V DC Steady-State Noise with a massive Short Circuit Cliff at x=12
        CLIFF_X = 12
        
        def signal_func(x):
            # Base 400V noise (scaled to fit graph)
            noise = 0.2 * np.sin(10 * x) + 0.1 * np.cos(25 * x) + np.random.normal(0, 0.05)
            # The Singularity (Short Circuit Drop)
            if x < CLIFF_X:
                return 1.5 + noise
            else:
                # Exponential decay drop
                return -1.5 + noise * 0.5 * np.exp(-(x - CLIFF_X))

        # Draw the static signal
        # We pre-calculate points to prevent numpy random jitter on every frame
        x_vals = np.linspace(0, 20, 1000)
        y_vals = [signal_func(x) for x in x_vals]
        
        signal_line = axes.plot_line_graph(
            x_values=x_vals, y_values=y_vals,
            line_color=COLOR_CYAN, stroke_width=3, add_vertex_dots=False
        )
        
        # Color the cliff and beyond Crimson
        cliff_line = axes.plot_line_graph(
            x_values=x_vals[x_vals >= CLIFF_X], y_values=y_vals[x_vals >= CLIFF_X],
            line_color=COLOR_CRIMSON, stroke_width=4, add_vertex_dots=False
        )

        self.safe_play(Create(signal_line), run_time=2)

        # The Wavelet Window and Ghost
        window_x = ValueTracker(2)
        
        window = always_redraw(lambda: Rectangle(
            width=2, height=5, color=WHITE, fill_opacity=0.1, stroke_width=2
        ).move_to(axes.c2p(window_x.get_value(), 0)))

        def db4_ghost(x_offset):
            # A scaled db4 approximation acting as the convolution kernel
            return lambda x: 0.8 * np.sin(5 * (x - x_offset)) * np.exp(-(x - x_offset)**2)

        ghost_wavelet = always_redraw(lambda: axes.plot(
            db4_ghost(window_x.get_value()), 
            x_range=[window_x.get_value()-1, window_x.get_value()+1],
            color=WHITE, stroke_width=2, stroke_opacity=0.5
        ))

        # Magnitude Meter
        meter_label = self.create_code_text("D1 MAGNITUDE: ", color=COLOR_CYAN_BR).scale(0.7)
        meter_value = DecimalNumber(0.05, num_decimal_places=2, color=COLOR_CYAN_BR, font_size=36)
        meter_group = VGroup(meter_label, meter_value).arrange(RIGHT).to_corner(DL, buff=SAFE_MARGIN)

        # Meter updater
        def update_meter(mob):
            x = window_x.get_value()
            if x < CLIFF_X - 0.5:
                # Random low noise
                val = 0.05 + np.random.uniform(0, 0.03)
                mob.set_value(val)
                mob.set_color(COLOR_CYAN_BR)
            elif x >= CLIFF_X - 0.5 and x <= CLIFF_X + 0.5:
                # The Spike
                val = 485.9 * np.exp(-10 * (x - CLIFF_X)**2)
                mob.set_value(val)
                if val > 100:
                    mob.set_color(COLOR_CRIMSON)
            else:
                mob.set_value(0.01)
                mob.set_color(COLOR_DIM_TEXT)

        meter_value.add_updater(update_meter)

        self.safe_play(FadeIn(window), FadeIn(ghost_wavelet), FadeIn(meter_group))

        # Slide across the normal noise
        self.play(window_x.animate.set_value(8), run_time=3, rate_func=linear)

        # ─────────────────────────────────────────────────────────
        # SCENE 4.2: THE SINGULARITY EVENT
        # ─────────────────────────────────────────────────────────
        # Slide to the cliff
        self.safe_play(FadeIn(cliff_line, run_time=0.1)) # Reveal crimson cliff dynamically
        self.play(window_x.animate.set_value(CLIFF_X), run_time=1.5, rate_func=ease_in_cubic)

        # Lock-on & Shatter effect
        shatter_flash = Rectangle(
            width=2.5, height=6, color=COLOR_CRIMSON, fill_opacity=0.6, stroke_width=0
        ).move_to(axes.c2p(CLIFF_X, 0))

        self.play(
            FadeIn(shatter_flash, rate_func=there_and_back, run_time=0.3),
            window.animate.scale(1.5).set_opacity(0),
            ghost_wavelet.animate.set_color(COLOR_CRIMSON).set_stroke(width=6)
        )
        meter_value.remove_updater(update_meter)
        meter_value.set_value(485.90)
        meter_value.set_color(COLOR_CRIMSON)

        # Mathematical Proof Overlay
        math_proof = MathTex(
            r"W_f(u, s) = \int_{-\infty}^{\infty} f(t) \frac{1}{\sqrt{s}} \psi\left(\frac{t-u}{s}\right) dt", 
            color=WHITE, font_size=36
        ).next_to(axes, DOWN, buff=0.5)
        
        lipschitz = self.create_code_text("LIPSCHITZ EXPONENT TRIGGERED.", color=COLOR_CRIMSON).scale(0.8)
        lipschitz.next_to(math_proof, DOWN, buff=0.2)

        self.safe_play(Write(math_proof), FadeIn(lipschitz, shift=UP))
        self.wait(1)

        # Final Tags
        tags = self.stack_vertical(
            self.create_kinetic_title("WAVELETS IGNORE THE WAVE."),
            self.create_kinetic_title("THEY ONLY SEE THE DISCONTINUITY.", color=COLOR_CRIMSON),
            buff=0.3, align_to=DOWN
        )
        
        self.safe_play(FadeOut(meter_group), Write(tags))
        self.check_overlaps()
        self.wait(3)