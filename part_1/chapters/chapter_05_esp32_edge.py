from manim import *
from core.base_scene import BaseChapter
from core.config import *

class Chapter05(BaseChapter):
    def construct(self):
        # ─────────────────────────────────────────────────────────
        # SCENE 5.1: LEGACY VS. EDGE SILICON
        # ─────────────────────────────────────────────────────────
        title = self.create_kinetic_title("[ THE ESP32 EDGE SILICON ]", color=COLOR_DIM_TEXT)
        title.to_corner(UL, buff=SAFE_MARGIN)
        self.safe_play(FadeIn(title))

        # Legacy Relay Box (Faked Isometric/Bulky 2D)
        legacy_box = VGroup(
            Rectangle(width=4, height=5, color=COLOR_DIM_TEXT, fill_opacity=0.3),
            Rectangle(width=3.5, height=1.5, color=COLOR_CYAN, fill_opacity=0.1).shift(UP*1), # Screen
            Circle(radius=0.3, color=COLOR_CRIMSON, fill_opacity=0.5).shift(DOWN*1 + LEFT*1), # Button
            Circle(radius=0.3, color=COLOR_GRID, fill_opacity=0.8).shift(DOWN*1 + RIGHT*1),
        ).move_to(ORIGIN)

        legacy_lbl = self.create_kinetic_title("[ PROPRIETARY FPGA: $20,000 ]", color=COLOR_DIM_TEXT).scale(0.6)
        legacy_lbl.next_to(legacy_box, UP, buff=0.5)

        self.safe_play(FadeIn(legacy_box, shift=UP), FadeIn(legacy_lbl))
        self.wait(1)

        # Laser Sweep Transformation
        laser = Line(UP*4, DOWN*4, color=COLOR_CYAN_BR, stroke_width=6).move_to(LEFT*5)
        
        # ESP32 Chip
        esp_chip = VGroup(
            RoundedRectangle(width=2, height=2, corner_radius=0.1, color=WHITE, fill_opacity=0.9, fill_color="#111"),
            Text("ESP32", font=FONT_SANS, weight=BOLD, font_size=24, color=WHITE)
        ).move_to(ORIGIN)

        esp_lbl = self.create_kinetic_title("[ COTS SILICON: $5.00 ]", color=COLOR_CYAN_BR).scale(0.6)
        esp_lbl.next_to(esp_chip, UP, buff=0.5)

        # The Sweep
        self.safe_play(FadeIn(laser))
        self.play(
            laser.animate.move_to(RIGHT*5),
            ReplacementTransform(legacy_box, esp_chip),
            ReplacementTransform(legacy_lbl, esp_lbl),
            run_time=1.5, rate_func=linear
        )
        self.safe_play(FadeOut(laser))
        self.wait(1)

        # ─────────────────────────────────────────────────────────
        # SCENE 5.2: ASYMMETRIC CORE ALLOCATION
        # ─────────────────────────────────────────────────────────
        self.safe_play(FadeOut(esp_lbl))
        
        # Split the chip into two cores
        core0 = VGroup(
            RoundedRectangle(width=2.5, height=2.5, corner_radius=0.1, color=COLOR_DIM_TEXT, fill_opacity=0.2),
            Text("CORE 0", font=FONT_MONO, font_size=24, color=COLOR_DIM_TEXT)
        )
        core1 = VGroup(
            RoundedRectangle(width=2.5, height=2.5, corner_radius=0.1, color=COLOR_CYAN, fill_opacity=0.2),
            Text("CORE 1", font=FONT_MONO, font_size=24, color=COLOR_CYAN_BR)
        )
        
        cores = VGroup(core0, core1).arrange(RIGHT, buff=2).move_to(UP*0.5)

        self.play(ReplacementTransform(esp_chip, cores), run_time=1)

        # Core 0: Slow WiFi/OS tasks (Orbiting packets)
        core0_lbl = self.create_code_text("OS / WiFi / Telemetry\n(Low Priority)", color=COLOR_DIM_TEXT).scale(0.5).next_to(core0, DOWN, buff=0.5)
        self.safe_play(FadeIn(core0_lbl))

        orbit_path = Circle(radius=1.8, color=COLOR_GRID).move_to(core0.get_center())
        packet = Dot(color=GREEN, radius=0.1)
        self.add(orbit_path, packet)
        
        # Orbit animation loop
        orbit_anim = MoveAlongPath(packet, orbit_path, run_time=3, rate_func=linear)
        self.play(orbit_anim)

        # Core 1: High-Speed Pinned DSP Engine
        core1_lbl = self.create_code_text("DSP Engine (Pinned)\n(Highest Priority)", color=COLOR_CYAN_BR).scale(0.5).next_to(core1, DOWN, buff=0.5)
        self.safe_play(FadeIn(core1_lbl))

        # Hardware Pins
        adc_pin = self.create_code_text("GPIO 36: ADC", color=WHITE).scale(0.5).to_edge(RIGHT).shift(UP*1.5)
        relay_pin = self.create_code_text("GPIO 17: RELAY", color=COLOR_CRIMSON).scale(0.5).to_edge(RIGHT).shift(DOWN*0.5)
        self.safe_play(FadeIn(adc_pin), FadeIn(relay_pin))

        # High speed data flow
        adc_line = DashedLine(adc_pin.get_left(), core1.get_right() + UP*1, color=COLOR_CYAN_BR)
        relay_line = Line(core1.get_right() + DOWN*1, relay_pin.get_left(), color=COLOR_CRIMSON, stroke_width=6)

        fast_packet = Dot(color=WHITE, radius=0.15)
        
        self.safe_play(Create(adc_line))
        
        # Rapid fire
        for _ in range(3):
            self.play(MoveAlongPath(fast_packet.copy(), adc_line), run_time=0.2, rate_func=linear)
        
        # Fault calculated -> Fire Relay
        self.play(Indicate(core1, color=COLOR_CRIMSON, scale_factor=1.1), run_time=0.3)
        self.safe_play(Create(relay_line), run_time=0.2)

        # Final Tags
        tags = self.stack_vertical(
            self.create_kinetic_title("DETERMINISTIC EXECUTION."),
            self.create_kinetic_title("ZERO OS INTERRUPTIONS.", color=COLOR_CYAN_BR),
            buff=0.3, align_to=DOWN
        )
        
        self.safe_play(Write(tags))
        
        # Keep orbiting in background while text finishes
        self.play(orbit_anim, run_time=2) 
        self.check_overlaps()