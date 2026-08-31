"""
Topic: Loss Functions and Optimization (Gradient Descent)
Visualizes the Cost Function as a "bowl" and shows a dot stepping down to the minimum.

To render in Google Colab, put this at the top of the cell:
%%manim -qh OptimizationVisual

Move the resulting .mp4 file to your assets/videos/ folder.
"""

from manim import *

class OptimizationVisual(Scene):
    def construct(self):
        # --- ACT 1: The Goal ---
        title = Text("Optimization: Minimizing Cost", font_size=40, weight=BOLD).to_edge(UP)
        self.play(Write(title))

        intro_text = Text("Goal: Find the weights that make the Cost (Error) as close to 0 as possible.", font_size=24, color=YELLOW).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(intro_text))

        # --- ACT 2: The Cost Landscape ---
        # Create a 2D Axes representing the Cost "Bowl"
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 16, 4],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": False},
        ).shift(DOWN * 0.5)

        x_label = axes.get_x_axis_label("w \\text{ (Model Weight)}", edge=RIGHT, direction=DOWN)
        y_label = axes.get_y_axis_label("J(w) \\text{ (Cost / Error)}", edge=UP, direction=LEFT)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # Draw a parabola: J(w) = w^2
        cost_curve = axes.plot(lambda x: x**2, color=BLUE)
        curve_label = axes.get_graph_label(cost_curve, "J(w) = w^2", x_val=3, direction=RIGHT)
        
        self.play(Create(cost_curve), run_time=2)
        self.play(Write(curve_label))
        self.wait(1)

        # --- ACT 3: The Blindfolded Hiker (Gradient Descent) ---
        # Starting point (High Error)
        start_w = 3.5
        start_point = axes.c2p(start_w, start_w**2)
        dot = Dot(point=start_point, color=RED, radius=0.15)
        dot_label = Text("Initial Random Guess\n(High Error!)", font_size=18, color=RED).next_to(dot, LEFT)

        self.play(FadeIn(dot), Write(dot_label))
        self.wait(1)

        # Show the gradient (Slope)
        tangent_line = TangentLine(cost_curve, alpha=0.9, length=3, color=YELLOW)
        grad_label = Text("Gradient (Slope) points uphill", font_size=18, color=YELLOW).next_to(tangent_line, UR)
        
        self.play(Create(tangent_line), Write(grad_label))
        self.wait(2)

        self.play(FadeOut(dot_label), FadeOut(grad_label), FadeOut(tangent_line))

        # Take steps down the mountain
        learning_rate = 0.15
        current_w = start_w

        step_text = Text("Action: Take steps in the OPPOSITE direction of the slope.", font_size=24, color=GREEN).next_to(axes, DOWN, buff=0.5)
        self.play(Write(step_text))

        # Animate 6 steps of gradient descent
        for i in range(6):
            # Derivative of w^2 is 2w
            gradient = 2 * current_w
            # Update rule: w = w - learning_rate * gradient
            next_w = current_w - learning_rate * gradient
            
            # Animate movement
            self.play(
                dot.animate.move_to(axes.c2p(next_w, next_w**2)),
                run_time=0.6,
                rate_func=linear
            )
            
            # Flash yellow to indicate a step taken
            flash = Flash(axes.c2p(next_w, next_w**2), color=YELLOW, flash_radius=0.3, line_length=0.1)
            self.play(flash, run_time=0.2)
            
            current_w = next_w

        self.wait(1)

        # Highlight the minimum
        min_text = Text("Global Minimum (Lowest Error)", font_size=24, color=GREEN).next_to(dot, UP)
        self.play(dot.animate.set_color(GREEN).scale(1.5), Write(min_text))
        
        self.wait(3)