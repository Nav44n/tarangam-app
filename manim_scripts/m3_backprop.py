from manim import *

class BackpropScene(Scene):
    def construct(self):
        # Nodes
        node_in = Circle(radius=0.5, color=BLUE).move_to(LEFT*3)
        node_hid = Circle(radius=0.5, color=BLUE).move_to(ORIGIN)
        node_out = Circle(radius=0.5, color=BLUE).move_to(RIGHT*3)
        
        # Edges
        edge1 = Arrow(node_in.get_right(), node_hid.get_left(), buff=0.1)
        edge2 = Arrow(node_hid.get_right(), node_out.get_left(), buff=0.1)
        
        # Labels
        w1_label = Text("w1", font_size=24).next_to(edge1, UP)
        w2_label = Text("w2", font_size=24).next_to(edge2, UP)
        
        self.play(FadeIn(node_in, node_hid, node_out))
        self.play(GrowArrow(edge1), GrowArrow(edge2))
        self.play(Write(w1_label), Write(w2_label))
        
        # Forward pass
        forward_dot = Dot(color=YELLOW)
        self.play(MoveAlongPath(forward_dot, edge1), run_time=1)
        self.play(MoveAlongPath(forward_dot, edge2), run_time=1)
        self.play(FadeOut(forward_dot))
        
        # Backward pass
        error_label = Text("δ(L)", color=RED, font_size=24).next_to(node_out, RIGHT)
        self.play(Write(error_label))
        
        backward_dot = Dot(color=RED)
        edge2_rev = Arrow(node_out.get_left(), node_hid.get_right(), buff=0.1, color=RED)
        edge1_rev = Arrow(node_hid.get_left(), node_in.get_right(), buff=0.1, color=RED)
        
        self.play(MoveAlongPath(backward_dot, edge2_rev), run_time=1)
        delta_hid = Text("δ(L)", color=RED, font_size=24).next_to(node_hid, DOWN)
        self.play(Write(delta_hid))
        self.play(MoveAlongPath(backward_dot, edge1_rev), run_time=1)
        
        self.wait(2)

