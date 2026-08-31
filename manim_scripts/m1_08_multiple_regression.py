"""
Topic: Linear Regression with Multiple Variables (Feature Scaling)
Visualizes the difference between Unscaled (Zig-Zag) and Scaled (Smooth) Gradient Descent.

Render Instructions for Google Colab:
-------------------------------------
Run this exactly in a Colab cell:

from manim import *

%%manim -qh FeatureScalingVisual

[paste the class code below here]

-------------------------------------
OUTPUT FILE:
Move the generated MP4 to: assets/videos/m1_08_multiple_regression.mp4
"""

from manim import *

class FeatureScalingVisual(Scene):
    def construct(self):
        # --- TITLE ---
        title = Text("Multiple Variables: Why We Scale Features", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        # --- ACT 1: Unscaled Data (The Zig-Zag) ---
        unscaled_title = Text("1. Unscaled Features (Size vs Bedrooms)", font_size=24, color=RED).shift(UP*2.5)
        self.play(FadeIn(unscaled_title))

        # Draw elongated contour "bowl" (Top-down view of the error valley)
        # Because Size is 1000x bigger than Bedrooms, the valley is stretched out
        contour1 = Ellipse(width=6, height=1.5, color=RED, fill_opacity=0.1)
        contour2 = Ellipse(width=4, height=1.0, color=RED, fill_opacity=0.2)
        contour3 = Ellipse(width=2, height=0.5, color=RED, fill_opacity=0.3)
        minimum_dot = Dot(color=YELLOW).move_to(contour3.get_center())

        unscaled_contours = VGroup(contour1, contour2, contour3, minimum_dot).shift(DOWN*0.5)
        self.play(Create(unscaled_contours))

        # Gradient Descent Path (Zig-Zagging)
        start_point = contour1.get_top() + RIGHT*2
        dot = Dot(point=start_point, color=WHITE)
        
        # Path representing poor convergence
        p1 = start_point + DOWN*1.2 + LEFT*0.5
        p2 = p1 + UP*0.8 + LEFT*1.0
        p3 = p2 + DOWN*0.6 + LEFT*0.8
        p4 = p3 + UP*0.4 + LEFT*0.6
        
        path1 = Arrow(start=start_point, end=p1, color=WHITE, buff=0.1, max_tip_length_to_length_ratio=0.15)
        path2 = Arrow(start=p1, end=p2, color=WHITE, buff=0.1, max_tip_length_to_length_ratio=0.15)
        path3 = Arrow(start=p2, end=p3, color=WHITE, buff=0.1, max_tip_length_to_length_ratio=0.15)
        path4 = Arrow(start=p3, end=p4, color=WHITE, buff=0.1, max_tip_length_to_length_ratio=0.15)

        self.play(FadeIn(dot))
        self.play(GrowArrow(path1), dot.animate.move_to(p1), run_time=0.7)
        self.play(GrowArrow(path2), dot.animate.move_to(p2), run_time=0.7)
        self.play(GrowArrow(path3), dot.animate.move_to(p3), run_time=0.7)
        self.play(GrowArrow(path4), dot.animate.move_to(p4), run_time=0.7)

        warning = Text("Gradient Descent struggles and zig-zags forever.", font_size=20, color=YELLOW).next_to(unscaled_contours, DOWN, buff=0.5)
        self.play(Write(warning))
        self.wait(2)

        # Clear screen
        self.play(FadeOut(unscaled_title), FadeOut(unscaled_contours), FadeOut(warning), 
                  FadeOut(dot), FadeOut(path1), FadeOut(path2), FadeOut(path3), FadeOut(path4))


        # --- ACT 2: Scaled Data (The Direct Path) ---
        scaled_title = Text("2. Scaled Features (Squished between -1 and 1)", font_size=24, color=GREEN).shift(UP*2.5)
        self.play(FadeIn(scaled_title))

        # Draw circular contour "bowl"
        c_contour1 = Circle(radius=2.5, color=GREEN, fill_opacity=0.1)
        c_contour2 = Circle(radius=1.5, color=GREEN, fill_opacity=0.2)
        c_contour3 = Circle(radius=0.5, color=GREEN, fill_opacity=0.3)
        c_minimum_dot = Dot(color=YELLOW).move_to(c_contour3.get_center())

        scaled_contours = VGroup(c_contour1, c_contour2, c_contour3, c_minimum_dot).shift(DOWN*0.5)
        self.play(Create(scaled_contours))

        # Gradient Descent Path (Direct)
        c_start_point = c_contour1.get_top() + RIGHT*1.5
        c_dot = Dot(point=c_start_point, color=WHITE)
        
        c_path1 = Arrow(start=c_start_point, end=c_contour2.get_top() + RIGHT*0.8, color=WHITE, buff=0.1, max_tip_length_to_length_ratio=0.15)
        c_path2 = Arrow(start=c_contour2.get_top() + RIGHT*0.8, end=c_contour3.get_top() + RIGHT*0.3, color=WHITE, buff=0.1, max_tip_length_to_length_ratio=0.15)
        c_path3 = Arrow(start=c_contour3.get_top() + RIGHT*0.3, end=c_minimum_dot.get_center(), color=WHITE, buff=0.1, max_tip_length_to_length_ratio=0.15)

        self.play(FadeIn(c_dot))
        self.play(GrowArrow(c_path1), c_dot.animate.move_to(c_contour2.get_top() + RIGHT*0.8), run_time=0.8)
        self.play(GrowArrow(c_path2), c_dot.animate.move_to(c_contour3.get_top() + RIGHT*0.3), run_time=0.8)
        self.play(GrowArrow(c_path3), c_dot.animate.move_to(c_minimum_dot.get_center()), run_time=0.8)
        
        flash = Flash(c_minimum_dot, color=YELLOW, flash_radius=0.5)
        self.play(flash)

        success = Text("Gradient Descent steps straight to the Global Minimum!", font_size=20, color=YELLOW).next_to(scaled_contours, DOWN, buff=0.5)
        self.play(Write(success))

        self.wait(3)