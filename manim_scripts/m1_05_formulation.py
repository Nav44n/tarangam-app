"""
Topic: Feature Representation and Problem Formulation
Visualizes translating a real-world object into a Feature Vector and passing it through f(x).

To render in Google Colab, put this at the top of the cell:
%%manim -qh Formulation

Move the resulting .mp4 file to your assets/videos/ folder.
"""

from manim import *

class Formulation(Scene):
    def construct(self):
        # --- ACT 1: Translating Reality to Math ---
        title = Text("Feature Representation", font_size=40, weight=BOLD).to_edge(UP)
        self.play(Write(title))

        # Real world object (House)
        house = SVGMobject("house.svg") if False else Square(color=BLUE, fill_opacity=0.5).scale(0.8).shift(LEFT*4 + UP*0.5)
        roof = Triangle(color=BLUE, fill_opacity=0.5).scale(0.9).next_to(house, UP, buff=0)
        real_house = VGroup(house, roof)
        
        house_label = Text("Real World Object", font_size=20).next_to(real_house, DOWN)
        self.play(FadeIn(real_house), Write(house_label))

        # Arrow indicating translation
        arrow = Arrow(start=LEFT*2, end=RIGHT*0.5, color=YELLOW)
        trans_text = Text("Extract Features", font_size=16, color=YELLOW).next_to(arrow, UP)
        self.play(GrowArrow(arrow), Write(trans_text))

        # The Feature Vector (x)
        vector_math = MathTex(
            r"x = \begin{bmatrix} 1500 \text{ sqft} \\ 3 \text{ beds} \\ \text{Red} \end{bmatrix}", 
            font_size=32
        ).shift(RIGHT*3 + UP*0.5)
        vector_label = Text("Feature Vector (x)", font_size=20, color=GREEN).next_to(vector_math, DOWN)
        
        self.play(Write(vector_math))
        self.play(Write(vector_label))
        self.wait(2)

        # --- ACT 2: One-Hot Encoding ---
        # Highlight the "Red" problem
        red_box = SurroundingRectangle(vector_math[0][-4:-1], color=RED, buff=0.1)
        error_text = Text("Error: Math cannot read 'Red'", font_size=16, color=RED).next_to(red_box, RIGHT)
        self.play(Create(red_box), Write(error_text))
        self.wait(1)

        # Transform to One-Hot
        one_hot_math = MathTex(
            r"x = \begin{bmatrix} 1500 \\ 3 \\ 1 \text{ (Is\_Red)} \\ 0 \text{ (Is\_Blue)} \\ 0 \text{ (Is\_Green)} \end{bmatrix}", 
            font_size=32
        ).move_to(vector_math)

        self.play(FadeOut(error_text), FadeOut(red_box))
        self.play(Transform(vector_math, one_hot_math))
        
        fix_text = Text("Fixed: One-Hot Encoding", font_size=16, color=GREEN).next_to(vector_math, RIGHT)
        self.play(Write(fix_text))
        self.wait(2)

        # --- ACT 3: The Formulation (f(x) -> y) ---
        self.play(
            FadeOut(real_house), FadeOut(house_label), FadeOut(arrow), FadeOut(trans_text), FadeOut(fix_text),
            title.animate.become(Text("Problem Formulation", font_size=40, weight=BOLD).to_edge(UP)),
            vector_math.animate.shift(LEFT*6).scale(0.8)
        )
        vector_label.next_to(vector_math, DOWN)

        # Hypothesis Function Box
        func_box = Rectangle(width=2, height=1.5, color=ORANGE, fill_opacity=0.2)
        func_text = MathTex("f(x)", font_size=36, color=ORANGE).move_to(func_box)
        func_label = Text("Hypothesis (Model)", font_size=18).next_to(func_box, UP)
        func_group = VGroup(func_box, func_text, func_label)
        
        arrow_in = Arrow(start=vector_math.get_right(), end=func_box.get_left(), buff=0.2)
        self.play(GrowArrow(arrow_in), FadeIn(func_group))

        # Output y
        output_y = MathTex(r"\hat{y} = \$300,000", font_size=36, color=GREEN).shift(RIGHT*4)
        output_label = Text("Predicted Output", font_size=18, color=GREEN).next_to(output_y, DOWN)
        
        arrow_out = Arrow(start=func_box.get_right(), end=output_y.get_left(), buff=0.2)
        
        self.play(GrowArrow(arrow_out))
        self.play(Write(output_y), Write(output_label))

        # Summary text
        summary = Text("Goal: Find the best f(x) that maps Inputs (x) to Outputs (y).", font_size=24, color=YELLOW).to_edge(DOWN, buff=1)
        self.play(Write(summary))

        self.wait(3)