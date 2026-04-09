# part_1/chapters/chapter_01_little_wave.py
# ─────────────────────────────────────────────────────────────────────
# CHAPTER 01 — THE CONCEPT OF THE "LITTLE WAVE"
# Fully corrected and production-ready implementation.
# ─────────────────────────────────────────────────────────────────────

from manim import *
import numpy as np
from core.base_scene import BaseChapter
from core.config import *


# ══════════════════════════════════════════════════════════════════════
#  STANDALONE HELPER FUNCTIONS
#  (pure functions — no scene state, always safe to call)
# ══════════════════════════════════════════════════════════════════════

def build_crt_wave(axes: Axes, func, color=COLOR_CYAN, t_offset: float = 0.0) -> VGroup:
    """
    Builds a 3-layer CRT-glow wave on the given axes.
    Each layer is an independent plot — no shared state.

    Args:
        axes:     The Axes object to plot on.
        func:     A lambda x -> y function.
        color:    Base color for the glow.
        t_offset: Time offset applied inside the lambda (caller-controlled).

    Returns:
        VGroup of [outer_glow, mid_glow, core_line]
    """
    layers = VGroup(
        axes.plot(func, color=color, stroke_width=10, stroke_opacity=0.10),
        axes.plot(func, color=color, stroke_width=5,  stroke_opacity=0.35),
        axes.plot(func, color=color, stroke_width=2,  stroke_opacity=1.00),
    )
    return layers


def build_db4_wave(axes: Axes, x_center: float = 7.5, color=COLOR_CYAN_BR) -> VGroup:
    """
    Builds the Daubechies-4 mother wavelet approximation centered at x_center.
    Returns a 2-layer CRT VGroup (glow + core).

    The db4 shape: sin(6*(x - x_center)) * gaussian_envelope
    """
    def db4(x):
        shifted = x - x_center
        envelope = np.exp(-(shifted ** 2) / 2.5)
        return np.sin(6.0 * shifted) * envelope

    glow = axes.plot(
        db4,
        color=COLOR_CYAN,
        stroke_width=14,
        stroke_opacity=0.18,
        x_range=[x_center - 3.5, x_center + 3.5],
    )
    core = axes.plot(
        db4,
        color=color,
        stroke_width=4,
        x_range=[x_center - 3.5, x_center + 3.5],
    )
    return VGroup(glow, core)


def build_fft_bar(axes: Axes, freq_x: float = 3.0, height: float = 2.0) -> VGroup:
    """
    Builds a single frequency bar (core + glow) on the FFT axes.

    Args:
        axes:   The Axes object (should be the fft_axes).
        freq_x: x-coordinate in data space for the bar center.
        height: Bar height in data units.

    Returns:
        VGroup of [glow_rect, core_rect]
    """
    center = axes.c2p(freq_x, height / 2.0)

    # Core bar
    core = Rectangle(
        width=0.25,
        height=axes.c2p(0, height)[1] - axes.c2p(0, 0)[1],
        color=COLOR_CYAN,
        fill_opacity=0.85,
        stroke_width=0,
    ).move_to(center)

    # Glow halo
    glow = Rectangle(
        width=0.45,
        height=core.height + 0.08,
        color=COLOR_CYAN,
        fill_opacity=0.18,
        stroke_width=0,
    ).move_to(core)

    return VGroup(glow, core)


# ══════════════════════════════════════════════════════════════════════
#  MAIN SCENE
# ══════════════════════════════════════════════════════════════════════

class Chapter01(BaseChapter):
    """
    Chapter 01: The Concept of the 'Little Wave'

    Scene 1.1 — The Fourier Failure (time-blindness)
    Scene 1.2 — The Mother Wavelet (db4 dilation & translation)
    """

    # ─────────────────────────────────────────────────────────────────
    # TOP-LEVEL ENTRY POINT
    # ─────────────────────────────────────────────────────────────────

    def construct(self):
        self._scene_1_1_fourier_failure()
        self._scene_1_2_mother_wavelet()

    # ─────────────────────────────────────────────────────────────────
    # SCENE 1.1 — THE FOURIER FAILURE
    # ─────────────────────────────────────────────────────────────────

    def _scene_1_1_fourier_failure(self):
        """
        Visualises why a pure Fourier spectrum cannot localise a
        microsecond transient spike in time.
        """

        # ── 1. Header label ──────────────────────────────────────────
        title = self.create_kinetic_title(
            "[ THE STANDARD: FOURIER TRANSFORM ]",
            color=COLOR_DIM_TEXT,
        )
        title.scale(0.55)
        title.to_corner(UL, buff=SAFE_MARGIN)

        self.play(FadeIn(title, shift=RIGHT * 0.4), run_time=1.2)

        # ── 2. Build axes ────────────────────────────────────────────
        wave_axes = Axes(
            x_range=[0, 15, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=11.0,
            y_length=2.8,
            axis_config={
                "color": COLOR_GRID,
                "stroke_width": 1.2,
                "include_ticks": False,
                "include_tip": False,
            },
        )
        wave_axes.shift(UP * 1.0)

        fft_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 3, 1],
            x_length=11.0,
            y_length=2.0,
            axis_config={
                "color": COLOR_GRID,
                "stroke_width": 1.2,
                "include_ticks": False,
                "include_tip": False,
            },
        )
        fft_axes.next_to(wave_axes, DOWN, buff=0.55)

        self.play(
            Create(wave_axes),
            Create(fft_axes),
            run_time=1.2,
        )

        # ── 3. Axis labels ───────────────────────────────────────────
        wave_label = Text("VOLTAGE", font=FONT_MONO, font_size=16, color=COLOR_DIM_TEXT)
        wave_label.next_to(wave_axes, LEFT, buff=0.15)

        fft_label = Text("SPECTRUM", font=FONT_MONO, font_size=16, color=COLOR_DIM_TEXT)
        fft_label.next_to(fft_axes, LEFT, buff=0.15)

        self.play(FadeIn(wave_label), FadeIn(fft_label), run_time=0.6)

        # ── 4. Initial steady-state sine wave ────────────────────────
        def steady_sine(x):
            return np.sin(3.0 * x)

        wave_mob = build_crt_wave(wave_axes, steady_sine, color=COLOR_CYAN)
        fft_bar  = build_fft_bar(fft_axes, freq_x=3.0, height=2.0)

        self.play(
            Create(wave_mob),
            GrowFromEdge(fft_bar, DOWN),
            run_time=1.5,
        )
        self.wait(0.4)

        # ── 5. Scroll the wave (time passing) ───────────────────────
        # We simulate scrolling by replacing the wave mob with
        # progressively time-shifted versions using a ValueTracker.
        time_tracker = ValueTracker(0.0)

        def redraw_wave() -> VGroup:
            t = time_tracker.get_value()
            return build_crt_wave(wave_axes, lambda x: np.sin(3.0 * x - t))

        live_wave = always_redraw(redraw_wave)

        # Swap static wave → live wave
        self.remove(wave_mob)
        self.add(live_wave)

        self.play(
            time_tracker.animate.set_value(6.0),
            run_time=3.0,
            rate_func=linear,
        )

        # ── 6. The transient spike ───────────────────────────────────
        # Capture current t so the spike is consistent with the wave.
        t_at_spike = time_tracker.get_value()

        def spike_sine(x):
            base = np.sin(3.0 * x - t_at_spike)
            bump = 2.2 * np.exp(-((x - 7.5) ** 2) / 0.015)
            return base + bump

        # Build spike overlay (drawn on top of the live wave)
        spike_mob = wave_axes.plot(
            spike_sine,
            color=COLOR_CRIMSON,
            stroke_width=3.5,
        )

        # Tiny twitch on the FFT bar — barely changes height
        fft_bar_twitch = build_fft_bar(fft_axes, freq_x=3.0, height=2.04)

        # Flash spike for two frames (0.04 s at 50 fps)
        self.play(
            FadeIn(spike_mob),
            Transform(fft_bar, fft_bar_twitch),
            run_time=0.06,
            rate_func=linear,
        )
        self.play(
            FadeOut(spike_mob),
            Transform(fft_bar, build_fft_bar(fft_axes, freq_x=3.0, height=2.0)),
            run_time=0.06,
            rate_func=linear,
        )

        # Continue scrolling after the spike
        self.play(
            time_tracker.animate.set_value(t_at_spike + 4.0),
            run_time=2.0,
            rate_func=linear,
        )

        # ── 7. Remove live_wave so we can safely fade everything ──────
        self.remove(live_wave)

        # ── 8. Kinetic typography — the verdict ──────────────────────
        fatal_title = self.create_kinetic_title(
            "FATAL FLAW: FOURIER IS TIME-BLIND.",
            color=COLOR_CRIMSON,
        )
        fatal_title.scale(0.62)

        subtext = Text(
            "Fourier integrates  −∞ → +∞.\n"
            "It knows the frequency EXISTS.\n"
            "It does NOT know  W H E N.",
            font=FONT_MONO,
            font_size=22,
            color=COLOR_DIM_TEXT,
            line_spacing=1.4,
        )
        fit_to_frame(subtext)

        verdict = VGroup(fatal_title, subtext)
        verdict.arrange(DOWN, buff=0.35)
        fit_to_frame(verdict)
        verdict.to_edge(DOWN, buff=0.55)

        self.play(FadeIn(verdict, scale=1.15), run_time=0.9)
        self.wait(2.5)

        # ── 9. Clear screen for Scene 1.2 ────────────────────────────
        self.play(
            FadeOut(title),
            FadeOut(wave_axes),
            FadeOut(fft_axes),
            FadeOut(wave_label),
            FadeOut(fft_label),
            FadeOut(fft_bar),
            FadeOut(verdict),
            run_time=0.9,
        )

    # ─────────────────────────────────────────────────────────────────
    # SCENE 1.2 — THE MOTHER WAVELET
    # ─────────────────────────────────────────────────────────────────

    def _scene_1_2_mother_wavelet(self):
        """
        Builds the db4 mother wavelet from particle debris,
        demonstrates dilation (scale) and translation (time-shift),
        and shows it locking onto a crimson glitch.
        """

        # ── 1. Re-create the wave axes (larger, centred) ─────────────
        wave_axes = Axes(
            x_range=[0, 15, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=12.0,
            y_length=3.5,
            axis_config={
                "color": COLOR_GRID,
                "stroke_width": 1.0,
                "include_ticks": False,
                "include_tip": False,
            },
        ).shift(DOWN * 0.2)

        self.play(Create(wave_axes), run_time=0.8)

        # ── 2. Sine-to-particles disintegration ──────────────────────
        def base_sine(x):
            return np.sin(3.0 * x)

        doomed_wave = build_crt_wave(wave_axes, base_sine)
        self.play(Create(doomed_wave), run_time=0.8)
        self.wait(0.3)

        # Sample 120 points along the core (index 2) of the wave
        n_particles = 120
        proportions = np.linspace(0, 1, n_particles)
        core_curve  = doomed_wave[2]    # the sharpest layer

        particle_origins = [
            core_curve.point_from_proportion(p) for p in proportions
        ]

        # Pre-compute random scatter targets (deterministic seed → reproducible)
        rng = np.random.default_rng(seed=42)
        scatter_offsets = rng.uniform(-1.0, 1.0, size=(n_particles, 2))

        scatter_targets = [
            origin + np.array([scatter_offsets[i, 0] * 5.0,
                                scatter_offsets[i, 1] * 2.5,
                                0.0])
            for i, origin in enumerate(particle_origins)
        ]

        particles = VGroup(*[
            Dot(point=particle_origins[i], color=COLOR_CYAN, radius=0.04)
            for i in range(n_particles)
        ])

        # Swap wave → particles
        self.play(
            FadeOut(doomed_wave),
            FadeIn(particles),
            run_time=0.4,
        )

        # Scatter
        scatter_anims = [
            particles[i].animate.move_to(scatter_targets[i])
            for i in range(n_particles)
        ]
        self.play(*scatter_anims, run_time=0.9, rate_func=rush_into)

        # ── 3. Assemble the db4 mother wavelet ───────────────────────
        #  x_center = 7.5  puts it visually in the middle of x_range [0,15]
        db4_mob = build_db4_wave(wave_axes, x_center=7.5)

        self.play(
            ReplacementTransform(particles, db4_mob),
            run_time=1.4,
        )
        self.wait(0.4)

        # ── 4. Dilation — LOW FREQUENCY (wide) ───────────────────────
        scale_label = Text(
            "SCALE (DILATION) — LOW FREQUENCY",
            font=FONT_MONO, font_size=24, color=COLOR_TEXT,
        )
        scale_label.to_edge(UP, buff=SAFE_MARGIN)
        fit_to_frame(scale_label)

        self.play(FadeIn(scale_label, shift=DOWN * 0.2), run_time=0.5)

        # Build a wider wavelet (x_center stays, envelope stretched)
        db4_wide = build_db4_wave(wave_axes, x_center=7.5, color=COLOR_CYAN_BR)
        # Manually stretch the wide version in x
        db4_wide.stretch(2.6, dim=0, about_point=wave_axes.c2p(7.5, 0))

        self.play(Transform(db4_mob, db4_wide), run_time=1.6)
        self.wait(0.4)

        # ── 5. Dilation — HIGH FREQUENCY (narrow) ────────────────────
        scale_label_high = Text(
            "SCALE (COMPRESSION) — HIGH FREQUENCY",
            font=FONT_MONO, font_size=24, color=COLOR_TEXT,
        )
        scale_label_high.to_edge(UP, buff=SAFE_MARGIN)
        fit_to_frame(scale_label_high)

        db4_narrow = build_db4_wave(wave_axes, x_center=7.5, color=COLOR_CYAN_BR)
        db4_narrow.stretch(0.32, dim=0, about_point=wave_axes.c2p(7.5, 0))

        self.play(
            Transform(scale_label, scale_label_high),
            Transform(db4_mob, db4_narrow),
            run_time=1.6,
        )
        self.wait(0.4)

        # Reset to normal-scale wavelet at the LEFT of the axis
        db4_reset = build_db4_wave(wave_axes, x_center=2.5)
        self.play(Transform(db4_mob, db4_reset), run_time=0.8)

        # ── 6. Translation (time-shift) ───────────────────────────────
        trans_label = Text(
            "TRANSLATION — TIME SHIFT",
            font=FONT_MONO, font_size=24, color=COLOR_TEXT,
        )
        trans_label.to_edge(UP, buff=SAFE_MARGIN)
        fit_to_frame(trans_label)

        self.play(Transform(scale_label, trans_label), run_time=0.6)

        # ── 7. Stationary crimson glitch on the timeline ──────────────
        glitch_x = 10.5       # data-space x coordinate of the fault

        glitch = wave_axes.plot(
            lambda x: 2.1 * np.exp(-((x - glitch_x) ** 2) / 0.04),
            color=COLOR_CRIMSON,
            stroke_width=4.5,
            x_range=[glitch_x - 0.8, glitch_x + 0.8],
        )

        self.play(FadeIn(glitch), run_time=0.5)

        # ── 8. Slide wavelet from x=2.5 to x=glitch_x ────────────────
        # We animate by building intermediate wavelet positions.
        # Using a ValueTracker that drives an always_redraw.
        center_tracker = ValueTracker(2.5)

        def redraw_db4() -> VGroup:
            xc = center_tracker.get_value()
            return build_db4_wave(wave_axes, x_center=xc)

        live_db4 = always_redraw(redraw_db4)

        self.remove(db4_mob)
        self.add(live_db4)

        self.play(
            center_tracker.animate.set_value(glitch_x),
            run_time=2.5,
            rate_func=linear,
        )

        # ── 9. Lock-on flash ─────────────────────────────────────────
        self.remove(live_db4)

        flash_mob = wave_axes.plot(
            lambda x: np.sin(6.0 * (x - glitch_x)) * np.exp(-((x - glitch_x) ** 2) / 2.5),
            color=WHITE,
            stroke_width=12,
            x_range=[glitch_x - 3.5, glitch_x + 3.5],
        )
        locked_db4 = build_db4_wave(wave_axes, x_center=glitch_x)

        self.add(locked_db4)
        self.play(
            FadeIn(flash_mob, rate_func=there_and_back),
            run_time=0.55,
        )
        self.remove(flash_mob)

        # ── 10. Final kinetic tag-lines ───────────────────────────────
        self.play(
            FadeOut(scale_label),
            FadeOut(wave_axes),
            FadeOut(glitch),
            FadeOut(locked_db4),
            run_time=0.7,
        )

        tag_finite   = self.create_kinetic_title("FINITE.",    color=COLOR_TEXT)
        tag_local    = self.create_kinetic_title("LOCALIZED.", color=COLOR_TEXT)
        tag_fast     = self.create_kinetic_title("FAST.",      color=COLOR_CYAN_BR)

        for tag in (tag_finite, tag_local, tag_fast):
            tag.scale(1.1)
            fit_to_frame(tag)

        tag_group = VGroup(tag_finite, tag_local, tag_fast)
        tag_group.arrange(DOWN, buff=0.45)
        fit_to_frame(tag_group)
        tag_group.move_to(ORIGIN)

        self.play(
            LaggedStart(
                FadeIn(tag_finite,  shift=RIGHT * 0.3, scale=1.2),
                FadeIn(tag_local,   shift=RIGHT * 0.3, scale=1.2),
                FadeIn(tag_fast,    shift=RIGHT * 0.3, scale=1.2),
                lag_ratio=0.25,
            ),
            run_time=1.4,
        )

        self.check_overlaps()
        self.wait(3.0)

        self.play(FadeOut(tag_group), run_time=0.8)