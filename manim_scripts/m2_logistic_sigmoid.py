from manim import *

class LogisticSigmoidScene(Scene):
    def construct(self):
        axes = Axes(x_range=[-6, 6, 1], y_range=[0, 1.2, 0.5], axis_config={"color": BLUE})
        
        sigmoid = axes.plot(lambda x: 1 / (1 + np.exp(-x)), color=YELLOW)
        label = Text("σ(z) = 1 / (1 + e^(-z))", color=YELLOW, font_size=24).to_corner(UL)
        
        # Decision boundary line at y=0.5
        boundary = axes.plot(lambda x: 0.5, color=RED)
        boundary_label = Text("Decision Boundary (0.5)", color=RED, font_size=20).next_to(boundary, UP)
        
        self.play(Create(axes))
        self.play(Create(sigmoid), Write(label))
        self.wait(1)
        self.play(Create(boundary), Write(boundary_label))
        
        # Dots
        dot_0 = Dot(axes.c2p(-3, 1/(1+np.exp(3))), color=WHITE)
        dot_1 = Dot(axes.c2p(3, 1/(1+np.exp(-3))), color=WHITE)
        
        self.play(FadeIn(dot_0), FadeIn(dot_1))
        self.wait(2)


