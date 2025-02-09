from manim import *

class TextDisplay(Scene):
    def __init__(self, text, font_size=48, v_align="center", h_align="center", **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_size = font_size
        self.v_align = v_align
        self.h_align = h_align

    def construct(self):
        screen = FullScreenRectangle()
        console.log(screen.width)
        text_mobject = Text(self.text, font_size=self.font_size)
        text_mobject.scale_to_fit_width(screen.width - 2 * LARGE_BUFF)

        # Alinhamento horizontal
        if self.h_align == "left":
            text_mobject.to_edge(LEFT)
        elif self.h_align == "right":
            text_mobject.to_edge(RIGHT)
        else:
            text_mobject.to_edge(ORIGIN)

        # Alinhamento vertical
        if self.v_align == "top":
            text_mobject.to_edge(UP)
        elif self.v_align == "bottom":
            text_mobject.to_edge(DOWN)
        else:
            text_mobject.to_edge(ORIGIN)

        self.play(Write(text_mobject))
        self.wait(2)

# Exemplo de uso
if __name__ == "__main__":
    scene = TextDisplay("Olá, Mundo!", font_size=64, v_align="top", h_align="left")
    scene.render()
