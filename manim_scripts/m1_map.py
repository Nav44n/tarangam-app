"""
Topic: Parameter Estimation - MAP (Maximum A Posteriori)
Visualizes the combination of Real Data and Prior Belief (Virtual Data), 
and demonstrates the "Tug of War" concept on a number line.

To render in high quality (1080p, 60fps), run:
manim -pqh manim_scripts/m1_map.py MAPEstimation -o m1_map.mp4

Move the resulting .mp4 file to your assets/videos/ folder.
"""

from manim import *

class MAPEstimation(Scene):
    def construct(self):
        # ==========================================
        # ACT 1: The Problem with MLE (Naive Logic)
        # ==========================================
        title = Text("Maximum A Posteriori (MAP)", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        mle_subtitle = Text("The Flaw of MLE", font_size=32, color=RED).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(mle_subtitle))

        # Show 3 coin flips (Real Data)
        real_data_text = Text("You flip a coin 3 times:", font_size=24).shift(UP*1)
        self.play(Write(real_data_text))

        # Create 3 Green Heads
        real_h1 = Circle(radius=0.5, color=GREEN, fill_opacity=0.5).shift(LEFT*1.5)
        real_h2 = Circle(radius=0.5, color=GREEN, fill_opacity=0.5)
        real_h3 = Circle(radius=0.5, color=GREEN, fill_opacity=0.5).shift(RIGHT*1.5)
        h_labels = VGroup(
            Text("H", font_size=36).move_to(real_h1),
            Text("H", font_size=36).move_to(real_h2),
            Text("H", font_size=36).move_to(real_h3)
        )
        real_coins = VGroup(real_h1, real_h2, real_h3, h_labels)
        self.play(FadeIn(real_coins, shift=DOWN))
        self.wait(1)

        # MLE Conclusion
        mle_calc = MathTex(r"\hat{p}_{MLE} = \frac{3 \text{ Heads}}{3 \text{ Total}} = 1.0 \text{ (100% Heads!)}", font_size=36)
        mle_calc.next_to(real_coins, DOWN, buff=0.8)
        self.play(Write(mle_calc))
        
        naive_text = Text("MLE blindly trusts small data. It thinks the coin is completely rigged.", font_size=20, color=YELLOW)
        naive_text.next_to(mle_calc, DOWN, buff=0.5)
        self.play(FadeIn(naive_text))
        self.wait(3)

        # Clear Act 1
        self.play(FadeOut(mle_subtitle), FadeOut(real_data_text), FadeOut(real_coins), FadeOut(mle_calc), FadeOut(naive_text))

        # ==========================================
        # ACT 2: Introducing the Prior (Virtual Data)
        # ==========================================
        map_subtitle = Text("The Fix: Introduce a 'Prior' Belief", font_size=32, color=BLUE).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(map_subtitle))

        prior_text = Text("Common Sense: Most coins are fair (50/50).", font_size=24).shift(UP*1)
        self.play(Write(prior_text))

        virtual_text = Text("Let's secretly add 'Virtual Data' before we calculate:", font_size=24, color=BLUE).next_to(prior_text, DOWN, buff=0.3)
        self.play(Write(virtual_text))

        # Create Virtual Coins (2 Heads, 2 Tails)
        virt_h1 = Circle(radius=0.4, color=BLUE, fill_opacity=0.3).shift(LEFT*2.25 + DOWN*0.5)
        virt_h2 = Circle(radius=0.4, color=BLUE, fill_opacity=0.3).shift(LEFT*0.75 + DOWN*0.5)
        virt_t1 = Circle(radius=0.4, color=BLUE, fill_opacity=0.3).shift(RIGHT*0.75 + DOWN*0.5)
        virt_t2 = Circle(radius=0.4, color=BLUE, fill_opacity=0.3).shift(RIGHT*2.25 + DOWN*0.5)
        
        v_labels = VGroup(
            Text("H", font_size=28).move_to(virt_h1),
            Text("H", font_size=28).move_to(virt_h2),
            Text("T", font_size=28).move_to(virt_t1),
            Text("T", font_size=28).move_to(virt_t2)
        )
        virtual_coins = VGroup(virt_h1, virt_h2, virt_t1, virt_t2, v_labels)
        
        self.play(FadeIn(virtual_coins, shift=UP))
        self.wait(2)

        # ==========================================
        # ACT 3: The Posterior Calculation (MAP)
        # ==========================================
        combine_text = Text("Combine Real Data + Virtual Data", font_size=28, color=YELLOW).next_to(virtual_coins, DOWN, buff=0.8)
        self.play(Write(combine_text))
        self.wait(1)

        # Bring back scaled-down real coins to combine
        real_coins.scale(0.8).next_to(virtual_coins, LEFT, buff=1)
        virtual_coins.next_to(real_coins, RIGHT, buff=0.5)
        
        # Adjust text layout
        self.play(FadeOut(prior_text), FadeOut(virtual_text), FadeOut(combine_text))
        
        # Label the groups
        real_label = Text("+ 3 Real (Green)", font_size=20, color=GREEN).next_to(real_coins, UP)
        virt_label = Text("+ 4 Virtual (Blue)", font_size=20, color=BLUE).next_to(virtual_coins, UP)
        self.play(FadeIn(real_coins), FadeIn(real_label), FadeIn(virt_label))
        
        # The MAP Math
        map_calc_1 = MathTex(r"\hat{p}_{MAP} = \frac{3 \text{ Real Heads} + 2 \text{ Virtual Heads}}{3 \text{ Real Total} + 4 \text{ Virtual Total}}", font_size=36)
        map_calc_1.shift(DOWN*1.5)
        self.play(Write(map_calc_1))
        self.wait(1)

        map_calc_2 = MathTex(r"\hat{p}_{MAP} = \frac{5}{7} = 0.71 \text{ (Much safer estimate!)}", font_size=36, color=YELLOW)
        map_calc_2.next_to(map_calc_1, DOWN, buff=0.5)
        self.play(Write(map_calc_2))
        self.wait(3)

        # Clear Act 2 & 3
        self.play(
            FadeOut(map_subtitle), FadeOut(real_coins), FadeOut(virtual_coins), 
            FadeOut(real_label), FadeOut(virt_label), FadeOut(map_calc_1), FadeOut(map_calc_2)
        )

        # ==========================================
        # ACT 4: The Tug of War Visualization
        # ==========================================
        tug_subtitle = Text("The Tug of War", font_size=32, color=YELLOW).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(tug_subtitle))

        # Number line from 0 to 1
        number_line = NumberLine(
            x_range=[0, 1.1, 0.1],
            length=10,
            color=WHITE,
            include_numbers=True,
            font_size=20
        ).shift(DOWN*0.5)
        self.play(Create(number_line))

        # Prior Dot (0.5)
        prior_dot = Dot(number_line.n2p(0.5), color=BLUE, radius=0.15)
        prior_label = Text("Prior (0.50)", font_size=20, color=BLUE).next_to(prior_dot, UP)
        self.play(FadeIn(prior_dot), Write(prior_label))

        # MLE Dot (1.0)
        mle_dot = Dot(number_line.n2p(1.0), color=RED, radius=0.15)
        mle_label = Text("MLE Data (1.00)", font_size=20, color=RED).next_to(mle_dot, UP)
        self.play(FadeIn(mle_dot), Write(mle_label))
        self.wait(1)

        # MAP Dot appearing in the middle
        map_dot = Dot(number_line.n2p(0.71), color=YELLOW, radius=0.2)
        map_label = Text("MAP (0.71)", font_size=24, color=YELLOW).next_to(map_dot, DOWN, buff=0.5)
        
        # Arrows showing the pull
        pull_left = Arrow(start=map_dot.get_center(), end=prior_dot.get_center(), color=BLUE, buff=0.2)
        pull_right = Arrow(start=map_dot.get_center(), end=mle_dot.get_center(), color=RED, buff=0.2)

        self.play(FadeIn(map_dot), Write(map_label))
        self.play(GrowArrow(pull_left), GrowArrow(pull_right))
        
        tug_expl = Text("The Prior pulls toward 0.5. The Data pulls toward 1.0.", font_size=24).shift(UP*1)
        self.play(Write(tug_expl))
        self.wait(3)

        # ==========================================
        # ACT 5: The Infinite Data Rule
        # ==========================================
        self.play(FadeOut(tug_expl), FadeOut(pull_left), FadeOut(pull_right))
        
        inf_expl = Text("What if we flip the coin 10,000 times?", font_size=28, color=GREEN).shift(UP*1)
        self.play(Write(inf_expl))

        # Animate MAP dot sliding towards MLE dot
        inf_math = MathTex(r"\hat{p}_{MAP} = \frac{10000 + 2}{10000 + 4} \approx 1.0", font_size=32).next_to(inf_expl, DOWN)
        self.play(Write(inf_math))

        self.play(
            map_dot.animate.move_to(number_line.n2p(0.999)),
            map_label.animate.next_to(number_line.n2p(0.999), DOWN, buff=0.5),
            run_time=2.5
        )

        final_text = Text("Rule: With infinite data, MAP becomes exactly MLE.", font_size=28, color=YELLOW).shift(DOWN*2.5)
        self.play(Write(final_text))

        self.wait(4)