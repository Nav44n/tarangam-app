from manim import *

class PCAScene(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5, 1], y_range=[-5, 5, 1])
        
        # Cloud of points (correlated)
        points = [
            (-3, -2.5), (-2, -1.8), (-1, -1.2), (0, 0.5), (1, 0.8), (2, 2.2), (3, 2.8)
        ]
        dots = VGroup(*[Dot(axes.c2p(x, y), color=BLUE) for x, y in points])
        
        self.play(Create(axes), FadeIn(dots))
        
        # Principal Component 1
        pc1 = Line(axes.c2p(-4, -4), axes.c2p(4, 4), color=YELLOW)
        pc1_label = Text("PC1 (Max Variance)", color=YELLOW, font_size=24).next_to(pc1, UP+LEFT)
        
        self.play(Create(pc1))
        self.play(Write(pc1_label))
        
        # Projections
        projections = VGroup()
        for x, y in points:
            # simple projection onto y=x
            proj_x = (x + y) / 2
            proj_y = proj_x
            line = DashedLine(axes.c2p(x, y), axes.c2p(proj_x, proj_y), color=GRAY)
            projections.add(line)
            
        self.play(Create(projections))
        self.wait(2)
