import json
from manim import *

class ArvoreConceitual(MovingCameraScene):
    def construct(self):
        # Carregar dados do arquivo JSON
        with open("dados_arvore.json", "r", encoding="utf-8") as f:
            dados = json.load(f)

        # Configuração inicial
        self.camera.background_color = BLACK

        # Centro do mapa (tronco da árvore)
        tronco = Circle(radius=0.5, color=WHITE, fill_color=GREEN, fill_opacity=0.8)
        tronco_texto = Text(dados["tronco"], color=WHITE).scale(0.5)
        tronco_group = VGroup(tronco, tronco_texto).move_to(ORIGIN)
        # Efeitos dinâmicos
        self.play(FadeIn(tronco_group))
        texto_explicativo = Text(
                dados["descricao_raiz"]
            ).scale(0.4).to_edge(DOWN)
        self.play(Write(texto_explicativo))

        # Desfocar e subir no tronco (categorias superiores)
        self.play(FadeOut(texto_explicativo))

        # Categorias principais representadas por objetos (raízes e ramos)
        categorias = dados["categorias"]
        outer_circle = Circle(radius=len(categorias)/2, color=BLUE, fill_color=BLUE, fill_opacity=0.8)
        angulos = [((360*DEGREES/len(categorias)) * n) for n in range(len(categorias))] 
#        self.play(GrowFromCenter(outer_circle))

        elementos = []
        for categoria in categorias:
            forma = categoria["forma"]  # Pode ser "circle", "square", etc.
            texto = categoria["texto"]
        
            posicao = outer_circle.point_at_angle(angulos.pop(0))

            if forma == "circle":
                shape = Circle(radius=0.4, color=WHITE, fill_color=BLUE, fill_opacity=0.7)
            elif forma == "square":
                shape = Square(side_length=0.8, color=WHITE, fill_color=BLUE, fill_opacity=0.7)
            else:
                shape = Circle(radius=0.4, color=WHITE, fill_color=GRAY, fill_opacity=0.7)  # Default

            categoria_texto = Text(texto, color=WHITE).scale(0.5).next_to(shape, DOWN)
            grupo = VGroup(shape, categoria_texto).move_to(posicao)
            elementos.append(grupo)

        # Linha do tempo (raízes descendo)
        linha_do_tempo = Line(start=DOWN*4, end=ORIGIN, color=GRAY, stroke_width=3)
        marco_texto = Text("Linha do Tempo", color=WHITE).scale(0.4).next_to(linha_do_tempo, LEFT)



        # Aparecer as categorias com textos
        for elemento in elementos:
            self.play(FadeIn(elemento))
        #self.play(tronco_group.animate.shift(UP * 1.5))
        #self.play(GrowFromCenter(linha_do_tempo))
        #self.play(Write(marco_texto))


        # Zoom dinâmico para descer nas raízes (categorias inferiores)
        self.camera.frame.save_state()
        for elemento in elementos:
            self.play(self.camera.frame.animate.scale(0.5).move_to(elemento.get_center()))
            self.play(Restore(self.camera.frame))

        self.play(self.camera.frame.animate.scale(1).move_to(ORIGIN))

        # Concluir com zoom para o tronco central
        self.play(FocusOn(tronco_group))
        self.wait(2)
