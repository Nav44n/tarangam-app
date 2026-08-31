from manim import *

class GradientDescentOptimizationScene(Scene):
    def construct(self):
        coordinate_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 9, 2],
            axis_config={"color": BLUE}
        )
        objective_parabola = coordinate_axes.plot(lambda x: x**2, color=WHITE)
        
        # Avoid get_graph_label because it defaults to MathTex
        function_label = Text("J(t) = t^2", font_size=24).next_to(objective_parabola, UP)
        
        optimization_dot = Dot(color=RED)
        initial_x = 2.5
        optimization_dot.move_to(coordinate_axes.c2p(initial_x, initial_x**2))
        
        self.play(Create(coordinate_axes), Create(objective_parabola), Write(function_label))
        self.play(FadeIn(optimization_dot))
        
        learning_rate = 0.4
        current_x = initial_x
        
        for iteration in range(4):
            gradient_step = 2 * current_x
            next_x = current_x - (learning_rate * gradient_step)
            next_position = coordinate_axes.c2p(next_x, next_x**2)
            
            self.play(
                optimization_dot.animate.move_to(next_position),
                run_time=1.2,
                rate_func=smooth
            )
            current_x = next_x
            
        self.wait(1)
