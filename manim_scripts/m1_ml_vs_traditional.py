"""
Topic: Machine Learning vs Traditional Programming
A 4-Act visual story explaining the paradigm shift and why hand-written rules fail.

To render in high quality (1080p, 60fps), run:
manim -pqh manim_scripts/m1_ml_vs_traditional.py MLParadigm -o m1_ml_vs_traditional.mp4
"""

from manim import *

class MLParadigm(Scene):
    def construct(self):
        # ==========================================
        # ACT 1: The Title
        # ==========================================
        title = Text("The Paradigm Shift", font_size=48, weight=BOLD, color=BLUE)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP, buff=0.5).scale(0.8))

        # ==========================================
        # ACT 2: Traditional Programming
        # ==========================================
        trad_title = Text("1. Traditional Programming", font_size=32, color=YELLOW).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(trad_title))

        # Boxes
        trad_data = Rectangle(width=2, height=1, color=WHITE).shift(LEFT*4 + UP*0.5)
        trad_data_text = Text("Data\n(Ingredients)", font_size=20, justify="center").move_to(trad_data)
        
        trad_rules = Rectangle(width=2, height=1, color=RED).shift(LEFT*4 + DOWN*1)
        trad_rules_text = Text("Rules\n(Recipe)", font_size=20, color=RED, justify="center").move_to(trad_rules)
        
        trad_comp = Rectangle(width=2.5, height=2.5, color=GRAY).shift(LEFT*0.5 + DOWN*0.25)
        trad_comp_text = Text("Computer", font_size=24, color=GRAY).move_to(trad_comp)
        
        trad_output = Rectangle(width=2, height=1, color=GREEN).shift(RIGHT*3.5 + DOWN*0.25)
        trad_output_text = Text("Output\n(Cake)", font_size=20, color=GREEN, justify="center").move_to(trad_output)

        # Arrows
        a1 = Arrow(start=trad_data.get_right(), end=trad_comp.get_left(), buff=0.2)
        a2 = Arrow(start=trad_rules.get_right(), end=trad_comp.get_left(), buff=0.2)
        a3 = Arrow(start=trad_comp.get_right(), end=trad_output.get_left(), buff=0.2)

        self.play(Create(trad_data), Write(trad_data_text), Create(trad_rules), Write(trad_rules_text))
        self.wait(1)
        self.play(Create(trad_comp), Write(trad_comp_text))
        self.play(GrowArrow(a1), GrowArrow(a2))
        
        # Gear processing
        gear = Text("⚙", font_size=60, color=WHITE).move_to(trad_comp)
        self.play(FadeOut(trad_comp_text), FadeIn(gear))
        self.play(Rotate(gear, angle=PI*2, run_time=1.5))
        
        self.play(GrowArrow(a3))
        self.play(Create(trad_output), Write(trad_output_text))
        self.wait(2)

        # Shrink and move up
        trad_group = VGroup(trad_title, trad_data, trad_data_text, trad_rules, trad_rules_text, trad_comp, gear, trad_output, trad_output_text, a1, a2, a3)
        self.play(trad_group.animate.scale(0.5).to_corner(UL).shift(DOWN*1))

        # ==========================================
        # ACT 3: Machine Learning
        # ==========================================
        ml_title = Text("2. Machine Learning", font_size=32, color=GREEN).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(ml_title))

        # Boxes (Flipped)
        ml_data = Rectangle(width=2, height=1, color=WHITE).shift(LEFT*4 + DOWN*1)
        ml_data_text = Text("Data\n(Ingredients)", font_size=20, justify="center").move_to(ml_data)
        
        ml_output = Rectangle(width=2, height=1, color=GREEN).shift(LEFT*4 + DOWN*2.5)
        ml_output_text = Text("Output\n(1000 Cakes)", font_size=20, color=GREEN, justify="center").move_to(ml_output)
        
        ml_comp = Rectangle(width=2.5, height=2.5, color=GRAY).shift(LEFT*0.5 + DOWN*1.75)
        gear_ml = Text("⚙", font_size=60, color=YELLOW).move_to(ml_comp)
        
        ml_rules = Rectangle(width=2, height=1, color=RED).shift(RIGHT*3.5 + DOWN*1.75)
        ml_rules_text = Text("Rules\n(The Model)", font_size=20, color=RED, justify="center").move_to(ml_rules)

        # Arrows
        a4 = Arrow(start=ml_data.get_right(), end=ml_comp.get_left(), buff=0.2)
        a5 = Arrow(start=ml_output.get_right(), end=ml_comp.get_left(), buff=0.2)
        a6 = Arrow(start=ml_comp.get_right(), end=ml_rules.get_left(), buff=0.2)

        self.play(Create(ml_data), Write(ml_data_text), Create(ml_output), Write(ml_output_text))
        self.wait(1)
        
        flip_expl = Text("Notice: We provide the Answers (Output) instead of the Rules.", font_size=20, color=YELLOW).next_to(ml_output, DOWN)
        self.play(Write(flip_expl))
        self.wait(2)

        self.play(Create(ml_comp), FadeIn(gear_ml))
        self.play(GrowArrow(a4), GrowArrow(a5))
        
        self.play(Rotate(gear_ml, angle=PI*4, run_time=2.5))
        
        self.play(GrowArrow(a6))
        self.play(Create(ml_rules), Write(ml_rules_text))
        self.wait(2)

        # ==========================================
        # ACT 4: Why do we need this? (Spam Example)
        # ==========================================
        self.play(FadeOut(trad_group), FadeOut(ml_title), FadeOut(flip_expl), 
                  FadeOut(ml_data), FadeOut(ml_data_text), FadeOut(ml_output), FadeOut(ml_output_text), 
                  FadeOut(ml_comp), FadeOut(gear_ml), FadeOut(ml_rules), FadeOut(ml_rules_text), 
                  FadeOut(a4), FadeOut(a5), FadeOut(a6))

        spam_title = Text("Why Traditional Fails: The Spam Problem", font_size=32, color=RED).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(spam_title))

        rule1 = Text("IF word == 'Viagra': Mark Spam", font_size=24, font="monospace").shift(UP*1)
        self.play(Write(rule1))
        self.wait(1)

        spam_reply = Text("Spammer: Sends 'V1agra'", font_size=24, color=YELLOW).next_to(rule1, DOWN)
        self.play(Write(spam_reply))
        
        cross = Cross(rule1, stroke_color=RED, stroke_width=6)
        self.play(Create(cross))

        rule2 = Text("IF word == 'V1agra': Mark Spam", font_size=24, font="monospace").next_to(spam_reply, DOWN)
        self.play(Write(rule2))
        
        spam_reply2 = Text("Spammer: Sends 'V-i-a-g-r-a'", font_size=24, color=YELLOW).next_to(rule2, DOWN)
        self.play(Write(spam_reply2))
        
        cross2 = Cross(rule2, stroke_color=RED, stroke_width=6)
        self.play(Create(cross2))
        self.wait(1)

        conclusion = Text("Conclusion: Hand-writing exact rules for fuzzy human logic is impossible.\nML learns the fuzzy patterns automatically.", font_size=24, color=GREEN, justify="center").shift(DOWN*3)
        self.play(Write(conclusion))

        self.wait(4)