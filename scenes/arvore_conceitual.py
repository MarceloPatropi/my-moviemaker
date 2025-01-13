import json
from manim import *

class ArvoreConceitual(MovingCameraScene):
    def construct(self):
        # Carregar dados do arquivo JSON
        with open("../dados_arvore.json", "r", encoding="utf-8") as f:
            dados = json.load(f)

        # Configuração inicial
        self.camera.background_color = ManimColor.from_hex("#013220")

        # Centro do mapa (tronco da árvore)
        tronco = Circle(radius=0.5, color=WHITE, fill_color=GREEN, fill_opacity=0.8)
        tronco_texto = Text(dados["texto"], color=WHITE).scale(0.5)
        tronco_group = VGroup(tronco, tronco_texto).move_to(ORIGIN)
        # Efeitos dinâmicos
        self.play(FadeIn(tronco_group))
        texto_explicativo = Text(
                dados["descricao_raiz"]
            ).scale(0.4).to_edge(DOWN)
        self.play(Write(texto_explicativo))

        # Desfocar e subir no tronco (categorias superiores)
        self.play(FadeOut(texto_explicativo))

        # Função recursiva para criar nós e seus filhos
        def criar_nos(categoria, posicao, angulo, raio):
            forma = categoria.get("forma", "circle")
            texto = categoria.get("texto", "")

            if forma == "circle":
                shape = Circle(radius=0.4, color=WHITE, fill_color=BLUE, fill_opacity=0.7)
            elif forma == "square":
                shape = Square(side_length=0.8, color=WHITE, fill_color=BLUE, fill_opacity=0.7)
            else:
                shape = Circle(radius=0.4, color=WHITE, fill_color=GRAY, fill_opacity=0.7)  # Default

            categoria_texto = Text(texto, color=WHITE).scale(0.5).next_to(shape, DOWN)
            grupo = VGroup(shape, categoria_texto).move_to(posicao)
            self.play(FadeIn(grupo))

            # Verificar e exibir subcategorias, se existirem
            if "filhos" in categoria and isinstance(categoria["filhos"], list) and categoria["filhos"]:
                filhos = categoria["filhos"]
                num_filhos = len(filhos)
                angulos_filhos = [angulo + (360*DEGREES/num_filhos) * n for n in range(num_filhos)]
                raio_filho = raio / 2

                for filho, angulo_filho in zip(filhos, angulos_filhos):
                    posicao_filho = posicao + np.array([raio_filho * np.cos(angulo_filho), raio_filho * np.sin(angulo_filho), 0])
                    criar_nos(filho, posicao_filho, angulo_filho, raio_filho)

            if "detalhes" in categoria:
                detalhes = categoria["detalhes"]
                titulo = Text(detalhes.get("titulo", ""), color=YELLOW).scale(0.6).to_edge(UP)
                contexto = Text(detalhes.get("contexto_historico", ""), color=WHITE).scale(0.4).next_to(titulo, DOWN)
                tecnicas = Text("\n".join(detalhes.get("tecnicas", [])), color=WHITE).scale(0.4).to_edge(DOWN)
                self.play(Write(titulo), Write(contexto))
                self.play(Write(tecnicas))

                # Esperar e remover
                self.wait(2)
                self.play(FadeOut(titulo), FadeOut(contexto), FadeOut(tecnicas))

        # Categorias principais representadas por objetos (raízes e ramos)
        categorias = dados["filhos"]
        outer_circle = Circle(radius=len(categorias)/2, color=BLUE, fill_color=BLUE, fill_opacity=0.8)
        angulos = [((360*DEGREES/len(categorias)) * n) for n in range(len(categorias))] 

        for categoria, angulo in zip(categorias, angulos):
            posicao = outer_circle.point_at_angle(angulo)
            criar_nos(categoria, posicao, angulo, len(categorias)/2)

        self.play(self.camera.frame.animate.scale(1).move_to(ORIGIN))

        # Concluir com zoom para o tronco central
        self.play(FocusOn(tronco_group))
        self.wait(2)
