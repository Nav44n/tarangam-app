"""
Topic: Parameter Estimation - MLE
A 4-Act visual explanation of the Likelihood function, the Log trick, and Calculus Optimization.

To render in high quality (1080p, 60fps), run:
manim -pqh manim_scripts/m1_mle.py MLERiggedCoin -o m1_mle.mp4
"""

from manim import *
import numpy as np

class MLERiggedCoin(Scene):
    def construct(self):
        # ==========================================
        # ACT 1: The Scenario
        # ==========================================
        title = Text("Maximum Likelihood Estimation", font_size=40, weight=BOLD, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))

        scenario = Text("You flip a coin 10 times. You get 7 Heads, 3 Tails.", font_size=24).next_to(title, DOWN, buff=0.5)
        question = Text("Question: What is the true bias (p) of this coin?", font_size=24, color=GREEN).next_to(scenario, DOWN, buff=0.2)
        self.play(FadeIn(scenario), Write(question))

        # Show the 10 coins
        coins = VGroup(*[Circle(radius=0.3, fill_opacity=0.8, color=GREEN if i<7 else RED) for i in range(10)]).arrange(RIGHT, buff=0.2).shift(DOWN*0.5)
        for i, c in enumerate(coins):
            lbl = Text("H" if i<7 else "T", font_size=20, color=BLACK).move_to(c)
            c.add(lbl)
        
        self.play(FadeIn(coins, shift=UP))
        self.wait(2)

        # ==========================================
        # ACT 2: The Likelihood Function
        # ==========================================
        self.play(FadeOut(coins), FadeOut(question), FadeOut(scenario))
        
        l_title = Text("Step 1: Write the Likelihood Function L(p)", font_size=28, color=BLUE).next_to(title, DOWN, buff=0.5)
        self.play(Write(l_title))

        formula1 = MathTex(r"L(p) = \text{Probability of getting exactly 7H, 3T}", font_size=32).shift(UP*1)
        formula2 = MathTex(r"L(p) = p \cdot p \cdot p \dots \cdot (1-p) \cdot (1-p) \cdot (1-p)", font_size=32).next_to(formula1, DOWN)
        formula3 = MathTex(r"L(p) = p^7 (1-p)^3", font_size=40, color=YELLOW).next_to(formula2, DOWN, buff=0.5)

        self.play(Write(formula1))
        self.wait(1)
        self.play(Write(formula2))
        self.wait(1)
        self.play(TransformFromCopy(formula2, formula3))
        self.wait(2)

        # ==========================================
        # ACT 3: Graphing the Curve (Finding the peak)
        # ==========================================
        self.play(FadeOut(formula1), FadeOut(formula2), formula3.animate.to_corner(UR).scale(0.8), FadeOut(l_title))
        
        graph_title = Text("Step 2: Find the parameter 'p' that maximizes L(p)", font_size=28, color=BLUE).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(graph_title))

        axes = Axes(
            x_range=[0, 1.1, 0.2], y_range=[0, 0.003, 0.001],
            x_length=8, y_length=4,
            axis_config={"include_numbers": False},
            x_axis_config={"numbers_to_include": [0, 0.5, 0.7, 1.0]}
        ).shift(DOWN*1)
        x_label = axes.get_x_axis_label("p \text{ (Bias of Coin)}", edge=RIGHT, direction=DOWN)
        y_label = axes.get_y_axis_label("L(p)", edge=UP, direction=LEFT)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label))

        def likelihood_func(p):
            if p < 0 or p > 1: return 0
            return (p**7) * ((1-p)**3)

        curve = axes.plot(likelihood_func, x_range=[0, 1], color=BLUE)
        self.play(Create(curve), run_time=2)

        # Animate dot climbing
        dot = Dot(color=RED).move_to(axes.c2p(0.1, likelihood_func(0.1)))
        dot_label = MathTex("p=0.1", font_size=24, color=RED).next_to(dot, UP)
        self.play(FadeIn(dot), FadeIn(dot_label))
        
        self.play(
            dot.animate.move_to(axes.c2p(0.4, likelihood_func(0.4))),
            dot_label.animate.next_to(axes.c2p(0.4, likelihood_func(0.4)), UP).become(MathTex("p=0.4", font_size=24, color=RED).next_to(axes.c2p(0.4, likelihood_func(0.4)), UP)),
            run_time=1.5
        )
        
        self.play(
            dot.animate.move_to(axes.c2p(0.7, likelihood_func(0.7))),
            dot_label.animate.next_to(axes.c2p(0.7, likelihood_func(0.7)), UP).become(MathTex(r"\hat{p}=0.7", font_size=28, color=GREEN).next_to(axes.c2p(0.7, likelihood_func(0.7)), UP)),
            run_time=1.5
        )

        # ==========================================
        # ACT 4: The Calculus (Derivative = 0)
        # ==========================================
        dot.set_color(GREEN)
        
        tangent_line = Line(start=axes.c2p(0.5, likelihood_func(0.7)), end=axes.c2p(0.9, likelihood_func(0.7)), color=YELLOW)
        tangent_label = Text("Derivative (Slope) = 0", font_size=20, color=YELLOW).next_to(tangent_line, RIGHT)
        self.play(Create(tangent_line), Write(tangent_label))
        
        dashed_line = DashedLine(start=axes.c2p(0.7, likelihood_func(0.7)), end=axes.c2p(0.7, 0), color=GREEN)
        self.play(Create(dashed_line))

        calc_expl = Text("In calculus, we find the exact peak by taking the derivative and setting it to 0.", font_size=20).next_to(axes, DOWN, buff=0.7)
        self.play(Write(calc_expl))

        # Final conclusion
        conclusion = Text("MLE Mathematically proves: p = 7/10 = 0.7", font_size=28, color=GREEN).next_to(calc_expl, DOWN)
        self.play(Write(conclusion))

        self.wait(4)