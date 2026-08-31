"""
Topic: The 4 ML Paradigms
A 4-Act visual showcase of Supervised, Unsupervised, Semi-supervised, and Reinforcement Learning.

To render in high quality (1080p, 60fps), run:
manim -pqh manim_scripts/m1_paradigms.py MLParadigms -o m1_paradigms.mp4
"""

from manim import *

class MLParadigms(Scene):
    def construct(self):
        # ==========================================
        # ACT 1: Title & Supervised Learning
        # ==========================================
        title = Text("The 4 Learning Paradigms", font_size=40, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title))

        sup_title = Text("1. Supervised Learning", font_size=32, color=BLUE).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(sup_title))

        sup_expl = Text("Data comes with explicit Answer Keys (Labels).", font_size=20).next_to(sup_title, DOWN)
        self.play(Write(sup_expl))

        # Create scattered shapes with labels
        apples = VGroup(*[Circle(color=RED, fill_opacity=0.8, radius=0.3).shift(LEFT*4 + UP*(i-1)*1.5 + RIGHT*np.random.uniform(-0.5,0.5)) for i in range(3)])
        oranges = VGroup(*[Circle(color=ORANGE, fill_opacity=0.8, radius=0.3).shift(RIGHT*4 + UP*(i-1)*1.5 + RIGHT*np.random.uniform(-0.5,0.5)) for i in range(3)])
        
        apple_labels = VGroup(*[Text("Apple", font_size=16).next_to(a, DOWN) for a in apples])
        orange_labels = VGroup(*[Text("Orange", font_size=16).next_to(o, DOWN) for o in oranges])

        self.play(FadeIn(apples), FadeIn(oranges))
        self.play(Write(apple_labels), Write(orange_labels))
        self.wait(1)

        # Model draws a classification boundary
        boundary = DashedLine(start=UP*3, end=DOWN*3, color=WHITE)
        b_text = Text("Learned Classification Boundary", font_size=16, color=GREEN).next_to(boundary, RIGHT).shift(UP*2)
        self.play(Create(boundary), Write(b_text))
        self.wait(2)

        self.play(FadeOut(apples), FadeOut(oranges), FadeOut(apple_labels), FadeOut(orange_labels), FadeOut(boundary), FadeOut(b_text), FadeOut(sup_title), FadeOut(sup_expl))

        # ==========================================
        # ACT 2: Unsupervised Learning
        # ==========================================
        unsup_title = Text("2. Unsupervised Learning", font_size=32, color=YELLOW).next_to(title, DOWN, buff=0.5)
        unsup_expl = Text("Raw Data ONLY. No Answer Keys. Find the hidden structure.", font_size=20).next_to(unsup_title, DOWN)
        self.play(FadeIn(unsup_title), Write(unsup_expl))

        # Scattered grey dots (no labels)
        dots = VGroup(*[Dot(color=LIGHT_GREY, radius=0.15).shift(np.random.uniform(-3, 3, 3) * [1, 0.5, 0]) for _ in range(25)])
        # Manually bias them into 3 clusters
        for i in range(8): dots[i].move_to(LEFT*4 + UP*1 + np.random.uniform(-1,1,3)*[1,1,0])
        for i in range(8, 16): dots[i].move_to(RIGHT*4 + UP*1 + np.random.uniform(-1,1,3)*[1,1,0])
        for i in range(16, 25): dots[i].move_to(DOWN*2 + np.random.uniform(-1,1,3)*[1,1,0])

        self.play(FadeIn(dots))
        self.wait(1.5)

        # AI identifies clusters
        c1 = Circle(color=RED).surround(dots[0:8], buffer_factor=1.2)
        c2 = Circle(color=BLUE).surround(dots[8:16], buffer_factor=1.2)
        c3 = Circle(color=GREEN).surround(dots[16:25], buffer_factor=1.2)

        self.play(Create(c1), Create(c2), Create(c3))
        self.play(
            dots[0:8].animate.set_color(RED),
            dots[8:16].animate.set_color(BLUE),
            dots[16:25].animate.set_color(GREEN)
        )
        c_text = Text("Algorithm automatically found 3 Clusters", font_size=20, color=YELLOW).next_to(c3, RIGHT, buff=0.5)
        self.play(Write(c_text))
        self.wait(2)

        self.play(FadeOut(dots), FadeOut(c1), FadeOut(c2), FadeOut(c3), FadeOut(c_text), FadeOut(unsup_title), FadeOut(unsup_expl))

        # ==========================================
        # ACT 3: Reinforcement Learning
        # ==========================================
        rl_title = Text("3. Reinforcement Learning", font_size=32, color=RED).next_to(title, DOWN, buff=0.5)
        rl_expl = Text("Learn by interacting with an Environment via Trial & Error.", font_size=20).next_to(rl_title, DOWN)
        self.play(FadeIn(rl_title), Write(rl_expl))

        # Gridworld Environment
        grid = NumberPlane(x_range=[0, 4, 1], y_range=[0, 3, 1], x_length=4, y_length=3, background_line_style={"stroke_color": WHITE}).shift(DOWN*1)
        self.play(Create(grid))

        agent = Dot(color=YELLOW, radius=0.2).move_to(grid.c2p(0.5, 0.5))
        agent_lbl = Text("Agent", font_size=16).next_to(agent, UP)
        
        fire = Square(color=RED, fill_opacity=0.8, side_length=0.8).move_to(grid.c2p(2.5, 0.5))
        fire_lbl = Text("-1 (Pain)", font_size=14, color=WHITE).move_to(fire)

        star = Star(color=GREEN, fill_opacity=0.8).scale(0.4).move_to(grid.c2p(3.5, 2.5))
        star_lbl = Text("+10 (Reward)", font_size=14, color=GREEN).next_to(star, UP)

        self.play(FadeIn(agent), FadeIn(agent_lbl), FadeIn(fire), FadeIn(fire_lbl), FadeIn(star), FadeIn(star_lbl))
        self.wait(1)

        # Agent moves into fire (Mistake)
        self.play(agent.animate.move_to(grid.c2p(1.5, 0.5)), run_time=0.5)
        self.play(agent.animate.move_to(grid.c2p(2.5, 0.5)), run_time=0.5)
        
        flash = Flash(fire, color=RED, flash_radius=0.5)
        self.play(flash)
        mistake_text = Text("Learned: Avoid this path!", font_size=16, color=RED).next_to(grid, RIGHT)
        self.play(Write(mistake_text))
        
        # Reset and succeed
        self.play(agent.animate.move_to(grid.c2p(0.5, 0.5)), FadeOut(mistake_text), run_time=1)
        
        # Optimal path
        path = [ (0.5, 1.5), (0.5, 2.5), (1.5, 2.5), (2.5, 2.5), (3.5, 2.5) ]
        for p in path:
            self.play(agent.animate.move_to(grid.c2p(*p)), run_time=0.3)
        
        flash2 = Flash(star, color=GREEN, flash_radius=0.5)
        self.play(flash2)
        success_text = Text("Learned: Optimal Policy!", font_size=20, color=GREEN).next_to(grid, RIGHT)
        self.play(Write(success_text))

        self.wait(3)