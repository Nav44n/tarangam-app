from manim import *

class KMeansScene(Scene):
    def construct(self):
        axes = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1])
        
        # Data points
        points = [
            (2,2), (2,3), (3,2),
            (7,7), (8,8), (7,8)
        ]
        dots = VGroup(*[Dot(axes.c2p(x, y), color=WHITE) for x, y in points])
        
        # Initial Centroids
        c1 = Dot(axes.c2p(5, 2), color=RED, radius=0.15)
        c2 = Dot(axes.c2p(5, 8), color=GREEN, radius=0.15)
        
        self.play(Create(axes), FadeIn(dots))
        self.play(FadeIn(c1), FadeIn(c2))
        self.wait(1)
        
        # Step 1: Assignment
        for i in range(3):
            dots[i].set_color(RED)
        for i in range(3, 6):
            dots[i].set_color(GREEN)
            
        self.wait(1)
        
        # Step 2: Update
        self.play(
            c1.animate.move_to(axes.c2p(7/3, 7/3)),
            c2.animate.move_to(axes.c2p(22/3, 23/3)),
            run_time=2
        )
        self.wait(2)
