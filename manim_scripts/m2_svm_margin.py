from manim import *

class SVMMarginScene(Scene):
    def construct(self):
        axes = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1], axis_config={"color": BLUE})
        
        # Data points
        class1 = VGroup(*[Dot(axes.c2p(x, y), color=RED) for x, y in [(2,8), (3,7), (2,6), (4,8)]])
        class2 = VGroup(*[Dot(axes.c2p(x, y), color=GREEN) for x, y in [(6,3), (7,4), (8,2), (7,2)]])
        
        # Hyperplanes
        decision_boundary = axes.plot(lambda x: -x + 11, color=WHITE)
        margin1 = axes.plot(lambda x: -x + 9, color=RED)
        margin2 = axes.plot(lambda x: -x + 13, color=GREEN)
        
        # Margin arrow
        p1 = axes.c2p(4.5, 6.5)
        p2 = axes.c2p(6.5, 4.5)
        margin_arrow = DoubleArrow(p1, p2, color=YELLOW, buff=0)
        margin_label = Text("2 / ||w||", color=YELLOW, font_size=24).next_to(margin_arrow, UP+RIGHT, buff=0.1)

        self.play(Create(axes))
        self.play(FadeIn(class1), FadeIn(class2))
        self.play(Create(decision_boundary))
        self.wait(1)
        self.play(Create(margin1), Create(margin2))
        self.play(GrowArrow(margin_arrow), Write(margin_label))
        self.wait(2)
