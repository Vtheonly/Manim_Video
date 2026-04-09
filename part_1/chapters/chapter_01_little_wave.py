from manim import *
import numpy as np
from core.base_scene import BaseChapter
from core.config import *

class Chapter01(BaseChapter):
    def construct(self):
        # ─────────────────────────────────────────────────────────
        # SCENE 1.1: THE FOURIER FAILURE
        # ─────────────────────────────────────────────────────────
        
        # 1. Title
        title_fourier = self.create_kinetic_title("[ THE STANDARD: FOURIER TRANSFORM ]", color=COLOR_DIM_TEXT)
        title_fourier.to_corner(UL, buff=SAFE_MARGIN)
        self.safe_play(FadeIn(title_fourier, shift=RIGHT), run_time=1.5)

        # 2. Axes Setup
        wave_axes = Axes(
            x_range=[0, 15, 1], y_range=[-2.5, 2.5, 1],
            x_length=12, y_length=3,
            axis_config={"color": COLOR_GRID, "stroke_width": 1, "include_ticks": False}
        ).shift(UP * 1.5)

        fft_axes = Axes(
            x_range=[0, 10, 1], y_range=[0, 3, 1],
            x_length=12, y_length=2.5,
            axis_config={"color": COLOR_GRID, "stroke_width": 1, "include_ticks": False}
        ).next_to(wave_axes, DOWN, buff=1.0)

        self.safe_play(Create(wave_axes), Create(fft_axes), run_time=1.5)

        # 3. Dynamic Wave & FFT
        time_tracker = ValueTracker(0)
        
        def get_sine_wave():
            t = time_tracker.get_value()
            # Faking a CRT glow by layering multiple lines
            wave = VGroup()
            for opacity, width in [(0.2, 8), (0.5, 4), (1.0, 2)]:
                w = wave_axes.plot(
                    lambda x: np.sin(3 * x - t), 
                    color=COLOR_CYAN, stroke_width=width, stroke_opacity=opacity
                )
                wave.add(w)
            return wave

        sine_wave = always_redraw(get_sine_wave)

        # The FFT Bar (Stationary because frequency doesn't change)
        fft_bar = Rectangle(width=0.3, height=2.0, color=COLOR_CYAN, fill_opacity=0.8)
        fft_bar.move_to(fft_axes.c2p(3, 1.0))
        fft_glow = Rectangle(width=0.5, height=2.1, color=COLOR_CYAN, fill_opacity=0.2).move_to(fft_bar)
        fft_group = VGroup(fft_glow, fft_bar)

        self.safe_play(FadeIn(sine_wave), GrowFromBottom(fft_group))
        
        # Scroll the wave
        self.play(time_tracker.animate.increment_value(5), run_time=3, rate_func=linear)

        # 4. The Microsecond Transient (Spike)
        # We simulate a massive spike appearing for exactly 1 frame
        spike_wave = wave_axes.plot(
            lambda x: np.sin(3 * x - time_tracker.get_value()) + (2.2 if 7.4 < x < 7.6 else 0), 
            color=COLOR_CRIMSON, stroke_width=4
        )
        
        # FFT barely twitches (visualizing time-blindness)
        twitch_bar = Rectangle(width=0.3, height=2.05, color=COLOR_CYAN, fill_opacity=0.8).move_to(fft_axes.c2p(3, 1.025))

        self.safe_play(Transform(sine_wave[2], spike_wave), Transform(fft_bar, twitch_bar), run_time=0.1)
        self.wait(0.1)
        self.safe_play(Restore(sine_wave[2]), Restore(fft_bar), run_time=0.1)

        # Continue scrolling
        self.play(time_tracker.animate.increment_value(3), run_time=2, rate_func=linear)

        # 5. Kinetic Typography Slam
        fatal_flaw = self.create_kinetic_title("FATAL FLAW: FOURIER IS TIME-BLIND.", color=COLOR_CRIMSON)
        subtext = self.create_code_text("Fourier integrates -∞ to +∞. It knows the frequency exists. It does NOT know WHEN.", color=COLOR_DIM_TEXT)
        subtext.scale(0.6) # Fit long text
        
        flaw_group = self.stack_vertical(fatal_flaw, subtext, buff=0.3, align_to=DOWN)
        
        self.safe_play(FadeIn(flaw_group, scale=1.5), run_time=0.8)
        self.wait(2)

        # ─────────────────────────────────────────────────────────
        # SCENE 1.2: THE MOTHER WAVELET
        # ─────────────────────────────────────────────────────────
        
        # Clean screen
        self.safe_play(
            FadeOut(title_fourier), FadeOut(flaw_group), FadeOut(fft_axes), FadeOut(fft_group),
            run_time=1
        )

        # Shatter the sine wave into particles
        particles = VGroup(*[
            Dot(point=sine_wave[2].point_from_proportion(alpha), color=COLOR_CYAN, radius=0.03)
            for alpha in np.linspace(0, 1, 150)
        ])
        self.safe_play(FadeOut(sine_wave), FadeIn(particles), run_time=0.5)

        # Random scatter
        self.play(particles.animate.apply_function(
            lambda p: p + np.array([np.random.uniform(-1, 1), np.random.uniform(-2, 2), 0])
        ), run_time=1)

        # Form the Daubechies 4 Wavelet
        def db4_approx(x):
            return np.sin(6 * x) * np.exp(-(x - 7.5)**2 / 2)
        
        db4_wavelet = wave_axes.plot(db4_approx, color=COLOR_CYAN_BR, stroke_width=5)
        db4_glow = wave_axes.plot(db4_approx, color=COLOR_CYAN, stroke_width=12, stroke_opacity=0.2)
        mother_wavelet = VGroup(db4_glow, db4_wavelet)

        self.safe_play(ReplacementTransform(particles, mother_wavelet), run_time=1.5)

        # The Breathing Math (Dilation)
        scale_label = self.create_code_text("SCALE (DILATION): LOW FREQUENCY", color=COLOR_TEXT).to_edge(UP)
        self.safe_play(FadeIn(scale_label, shift=DOWN))
        
        # Stretch horizontal
        self.play(mother_wavelet.animate.stretch(2.5, dim=0), run_time=1.5, rate_func=there_and_back)
        
        # Squish horizontal
        scale_label_high = self.create_code_text("SCALE (COMPRESSION): HIGH FREQUENCY", color=COLOR_TEXT).to_edge(UP)
        self.play(Transform(scale_label, scale_label_high), mother_wavelet.animate.stretch(0.3, dim=0), run_time=1.5)
        self.wait(0.5)

        # Translation over a glitch
        trans_label = self.create_code_text("TRANSLATION (TIME SHIFT)", color=COLOR_TEXT).to_edge(UP)
        self.play(Transform(scale_label, trans_label), mother_wavelet.animate.move_to(wave_axes.c2p(2, 0)), run_time=1)

        # Stationary glitch
        glitch = wave_axes.plot(lambda x: 1.5 * np.exp(-(x - 10)**2 / 0.05), color=COLOR_CRIMSON, stroke_width=4)
        self.safe_play(FadeIn(glitch))

        # Slide over it
        self.play(mother_wavelet.animate.move_to(wave_axes.c2p(10, 0)), run_time=2)
        
        # Lock on & Glow
        blinding_glow = wave_axes.plot(db4_approx, color=WHITE, stroke_width=10).move_to(wave_axes.c2p(10, 0))
        self.safe_play(FadeIn(blinding_glow, rate_func=there_and_back), run_time=0.5)

        # Final Kinetic tags
        tags = self.stack_vertical(
            self.create_kinetic_title("FINITE."),
            self.create_kinetic_title("LOCALIZED."),
            self.create_kinetic_title("FAST.", color=COLOR_CYAN_BR),
            buff=0.3, align_to=DOWN
        )
        
        self.safe_play(FadeOut(scale_label), Write(tags))
        self.check_overlaps()
        self.wait(3)