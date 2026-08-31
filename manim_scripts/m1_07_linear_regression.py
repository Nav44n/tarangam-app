"""
Topic: Linear Regression with One Variable
Visualizes data points, a shifting line of best fit, and the residuals (errors) being minimized.

To render in Google Colab, put this at the top of the cell:
%%manim -qh LinearRegressionVisual

Move the resulting .mp4 file to your assets/videos/ folder.
"""

from manim import *

class LinearRegressionVisual(Scene):
    def construct(self):
        # --- ACT 1: The Data ---
        title = Text("Linear Regression", font_size=40, weight=BOLD).to_edge(UP)
        self.play(Write(title))

        # Create a 2D Axes representing House Size vs Price
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=7,
            y_length=5,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5)

        x_label = axes.get_x_axis_label("x \\text{ (House Size)}", edge=RIGHT, direction=DOWN)
        y_label = axes.get_y_axis_label("y \\text{ (Price)}", edge=UP, direction=LEFT)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # Data points (x, y)
        data = [(1, 1.5), (2, 2.5), (3, 2.0), (4, 4.5), (5, 4.0)]
        dots = VGroup(*[Dot(axes.c2p(x, y), color=YELLOW) for x, y in data])
        
        self.play(FadeIn(dots, shift=UP))
        self.wait(1)

        # --- ACT 2: A Bad Fit Line ---
        bad_w0 = 1.0
        bad_w1 = 0.2
        bad_line = axes.plot(lambda x: bad_w0 + bad_w1 * x, color=RED, x_range=[0, 6])
        line_label = MathTex(r"\hat{y} = w_0 + w_1x", color=RED).next_to(bad_line, UP, buff=0.1).shift(LEFT*2)

        self.play(Create(bad_line), Write(line_label))
        
        bad_text = Text("A bad guess creates huge errors.", font_size=20, color=RED).next_to(title, DOWN)
        self.play(FadeIn(bad_text))

        # Show residuals (errors)
        residuals = VGroup()
        for x, y in data:
            pred_y = bad_w0 + bad_w1 * x
            line = DashedLine(
                start=axes.c2p(x, y),
                end=axes.c2p(x, pred_y),
                color=RED
            )
            residuals.add(line)
        
        self.play(Create(residuals))
        self.wait(2)

        # --- ACT 3: Minimizing the Errors (Least Squares) ---
        self.play(FadeOut(bad_text))
        opt_text = Text("Least Squares finds the line that minimizes the squared errors.", font_size=20, color=GREEN).next_to(title, DOWN)
        self.play(FadeIn(opt_text))

        # Animate the line shifting to the best fit
        # Best fit for this data is approx: w0 = 0.5, w1 = 0.7
        best_w0 = 0.5
        best_w1 = 0.7
        
        best_line = axes.plot(lambda x: best_w0 + best_w1 * x, color=GREEN, x_range=[0, 6])
        best_label = MathTex(r"\hat{y} = 0.5 + 0.7x", color=GREEN).move_to(line_label)

        # Update function for residuals to animate them dynamically as the line moves
        def update_residuals(res):
            new_res = VGroup()
            current_line = bad_line  # It transforms, so we track the visual line points
            
            # Since bad_line is transforming into best_line, we calculate the intermediate y
            # by interpolating between the bad weights and good weights.
            # Manim handles the line transform natively, but we need custom logic for the dashed lines.
            pass # (Simplified for Manim compatibility without ValueTrackers to prevent complex errors)

        # We will fade out old residuals, transform the line, and fade in new tiny residuals
        self.play(FadeOut(residuals))
        self.play(
            Transform(bad_line, best_line),
            Transform(line_label, best_label),
            run_time=2
        )

        new_residuals = VGroup()
        for x, y in data:
            pred_y = best_w0 + best_w1 * x
            line = DashedLine(
                start=axes.c2p(x, y),
                end=axes.c2p(x, pred_y),
                color=GREEN
            )
            new_residuals.add(line)
        
        self.play(Create(new_residuals))
        
        final_text = Text("Best Fit (Global Minimum of Cost Function)", font_size=20, color=YELLOW).next_to(axes, DOWN)
        self.play(Write(final_text))
        
        self.wait(3)