from manim import *

class MapaMental(Scene):
    def construct(self):
        titulo = Text("Mapa Mental: A Alma no Laboratório", font_size=36)
        self.play(Write(titulo))
        self.wait(1)
        self.play(titulo.animate.to_edge(UP))

        # Adicionar nós e subtópicos
        nodes = [
            ("A Alma no Laboratório", []),
            ("Origens do Conceito de Alma", ["Filosofia Clássica", "Idade Média"]),
            ("Renascimento e Racionalismo", ["Descartes", "Spinoza"]),
            ("Psicofísica", ["Fechner", "Weber"]),
            ("Laboratório de Wundt", ["Estruturalismo", "Funcionalismo"]),
            ("Conclusão", [])
        ]

        # Calcular posições com base na quantidade de subtópicos
        base_position = UP * 2
        vertical_spacing = 1.5
        positions = []
        current_position = base_position

        for node, subnodes in nodes:
            positions.append(current_position.copy())  # Adicionar a posição atual à lista
            # Ajustar a posição para o próximo tópico principal
            current_position += (vertical_spacing + len(subnodes) * 0.75) * DOWN

        dots = []
        for i, ((node, subnodes), pos) in enumerate(zip(nodes, positions)):
            dot = Dot(pos + LEFT*2)
            label = Text(node, font_size=24).next_to(dot, LEFT)
            dots.append((dot, label))
            self.play(FadeIn(dot), Write(label))
            if i > 0:
                self.play(Create(Line(dots[i-1][0].get_center(), dot.get_center())))

            # Adicionar subtópicos
            sub_pos = pos + RIGHT*2
            for subnode in subnodes:
                sub_dot = Dot(sub_pos)
                sub_label = Text(subnode, font_size=20).next_to(sub_dot, RIGHT)
                self.play(FadeIn(sub_dot), Write(sub_label))
                self.play(Create(Line(dot.get_center(), sub_dot.get_center())))
                sub_pos += DOWN*0.75  # Corrigir a direção do deslocamento para baixo

        self.wait(2)
