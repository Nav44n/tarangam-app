"""
Manim scene for topic m1-mle ("Maximum Likelihood Estimation").
Renders the log-likelihood curve for the 10-toss, 7-heads coin example
and animates the maximum being located at p = 0.7.

Render with:
    manim -pql m1_mle_hill_climb.py MLEHillClimb
(drop -p to not auto-preview; use -qh for a high-quality render)

Output the finished file as m1_mle_hill_climb.mp4 into the app's
assets/videos/ folder, then point the corresponding video-slot's
`script` path at it — the front end will pick it up automatically.
"""
from manim import *
import numpy as np

class MLEHillClimb(Scene):
    def construct(self):
        title = Text("MLE: log-likelihood of a coin's bias", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0.01, 0.99, 0.1],
            y_range=[-12, -6, 1],
            x_length=9, y_length=5,
            axis_config={"include_tip": True},
        ).shift(DOWN * 0.4)
        x_label = axes.get_x_axis_label("p")
        y_label = axes.get_y_axis_label(r"\ell(p)")
        self.play(Create(axes), Write(x_label), Write(y_label))

        k, n = 7, 10
        def loglik(p):
            p = np.clip(p, 1e-4, 1 - 1e-4)
            return k * np.log(p) + (n - k) * np.log(1 - p)

        curve = axes.plot(loglik, color=BLUE, x_range=[0.05, 0.95])
        self.play(Create(curve), run_time=2)

        dot = Dot(color=YELLOW).move_to(axes.c2p(0.1, loglik(0.1)))
        self.play(FadeIn(dot))

        # climb the curve toward the maximum at p = 0.7
        for p in np.linspace(0.1, 0.7, 8):
            self.play(dot.animate.move_to(axes.c2p(p, loglik(p))), run_time=0.35)

        peak_label = MathTex(r"\hat p_{MLE} = 0.7").next_to(dot, UP)
        self.play(Write(peak_label))
        self.wait(1.5)
