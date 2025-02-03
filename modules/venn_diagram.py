from manim import *
import numpy as np

class VennDiagram(Scene):
    def __init__(self, set_labels=None, set_colors=None, intersection_labels=None, shift_multiplier=1.5, **kwargs):
        super().__init__(**kwargs)
        self.set_labels = set_labels or ["A", "B"]
        self.set_colors = set_colors or [BLUE, GREEN]
        self.intersection_labels = intersection_labels or {}
        self.shift_multiplier = shift_multiplier
        self.num_sets = len(self.set_labels)
        if len(self.set_colors) < self.num_sets:
            raise ValueError("O número de cores deve ser igual ou maior que o número de conjuntos.")

    def construct(self):
        circles = []
        labels = []

        # Calcular o tamanho da fonte com base na label mais longa
        max_label_length = max(len(label) for label in self.set_labels + list(self.intersection_labels.values()))
        font_size = max(24, 48 - max_label_length * 2)

        # Criar os círculos do diagrama de Venn
        for i in range(self.num_sets):
            angle = i * TAU / self.num_sets
            circle = Circle(radius=2, color=self.set_colors[i], fill_opacity=0.5)
            circle.shift(self.shift_multiplier * np.array([np.cos(angle), np.sin(angle), 0]))
            circles.append(circle)
            label = Text(self.set_labels[i], font_size=font_size).move_to(circle.get_center())
            labels.append(label)

        # Adicionar os círculos e rótulos à cena, um de cada vez
        for circle, label in zip(circles, labels):
            self.play(Create(circle))
            self.play(Write(label))

        # Adicionar interseções
        intersections = []
        for i in range(self.num_sets):
            for j in range(i + 1, self.num_sets):
                intersection = Intersection(circles[i], circles[j], color=YELLOW, fill_opacity=0.5)
                intersection_label = self.intersection_labels.get((i, j), f"{self.set_labels[i]} ∩ {self.set_labels[j]}")
                intersection_text = Text(intersection_label, font_size=font_size).move_to(intersection.get_center())
                intersections.append((intersection, intersection_text))

        # Adicionar interseções à cena
        for intersection, intersection_text in intersections:
            self.play(Create(intersection), Write(intersection_text))

        # Manter a animação por alguns segundos
        self.wait(2)

# Exemplo de uso
if __name__ == "__main__":
    intersection_labels = {
        (0, 1): "Interseção A ∩ B",
        (1, 2): "Interseção B ∩ C",
        (0, 2): "Interseção A ∩ C"
    }
    scene = VennDiagram(set_labels=["A", "B", "C"], set_colors=[BLUE, GREEN, RED], intersection_labels=intersection_labels, shift_multiplier=1.5)
    scene.render()