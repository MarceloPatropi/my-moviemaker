import sys
import os
import json
from manim import *

from modules.arvore_conceitual import ArvoreConceitual
from modules.venn_diagram import VennDiagram
from modules.elevenlabs_tts import ElevenLabsTTS
from modules.pexels_api import PexelsAPI

class VideoWundt(Scene):
    def construct(self):
        # Criar Diagrama de Venn com Filosofia, Teologia e Ciência
        venn = VennDiagram(
            set_labels=["Filosofia", "Teologia", "Ciência"],
            set_colors=[BLUE, GREEN, RED],
            intersection_labels={
                (0, 1): "Dualismo",
                (1, 2): "Fé vs. Empirismo",
                (0, 2): "Mente racional",
                (0, 1, 2): "Alma"
            },
            shift_multiplier=1.5
        ).to_edge(UP)
        self.add(venn)
        self.play(FadeIn(venn))
        self.wait(2)

        # Criar Árvore Conceitual destacando "Alma" e "Mente"
        arvore = ArvoreConceitual("data/dados_arvore.json")
        arvore.to_edge(DOWN)
        self.add(arvore)
        self.play(FadeOut(venn), FadeIn(arvore))
        self.wait(2)

        # Destacar a transição "Alma" -> "Mente"
        arvore.highlight_node("Alma", color=YELLOW)
        self.wait(2)
        arvore.change_text("Alma", "Mente")
        self.wait(2)

        # Finalizar animação
        self.play(FadeOut(arvore))

def gerar_audio():
    tts = ElevenLabsTTS()
    roteiro = """
    O que é a alma? Desde a antiguidade, filósofos, teólogos e cientistas tentaram responder essa pergunta. 
    Para Platão, a alma era imortal. Para Descartes, separada do corpo. Mas no século XIX, Wilhelm Wundt trouxe uma nova abordagem. 
    A Psicologia experimental transformou o estudo da alma em algo mensurável.
    """
    audio_file = "output/narracao_wundt.mp3"
    audio = tts.generate_audio(roteiro, output_file=audio_file)
    tts.save_audio(audio, audio_file)
    print(f"Áudio gerado: {audio_file}")

def buscar_midias():
    pexels = PexelsAPI()
    imagens = pexels.search_photos("filosofia", per_page=3)
    videos = pexels.search_videos("ciência", per_page=3)

    assets = {
        "imagens": [img["src"]["original"] for img in imagens["photos"]],
        "videos": [vid["video_files"][0]["link"] for vid in videos["videos"]]
    }

    with open("data/pexels_wundt.json", "w") as f:
        json.dump(assets, f, indent=4)

    print("Mídias do Pexels salvas em 'data/pexels_wundt.json'.")

def gerar_json_edicao():
    edicao = {
        "audio": "output/narracao_wundt.mp3",
        "animacoes": ["output/video_venn.mp4", "output/video_arvore.mp4"],
        "imagens": "data/pexels_wundt.json",
        "tempo": {
            "venn_aparece": 0,
            "venn_sai": 5,
            "arvore_aparece": 6,
            "destacar_alma": 8,
            "mudar_para_mente": 10
        }
    }

    with open("data/edicao_wundt.json", "w") as f:
        json.dump(edicao, f, indent=4)

    print("JSON de edição salvo em 'data/edicao_wundt.json'.")

if __name__ == "__main__":
    print("Gerando animações...")
    #scene = VideoWundt()
    #scene.render()

    venn = VennDiagram(
        set_labels=["Filosofia", "Teologia", "Ciência"],
        set_colors=[BLUE, GREEN, RED],
        intersection_labels={
            (0, 1): "Dualismo",
            (1, 2): "Fé vs. Empirismo",
            (0, 2): "Mente racional",
            (0, 1, 2): "Alma"
        },
        shift_multiplier=1.5
    )
#    venn.render("output/video_venn.mp4")

    print("Gerando áudio da narração...")
#    gerar_audio()

    print("Buscando imagens e vídeos no Pexels...")
    buscar_midias()

    print("Criando JSON para edição no Premiere...")
#    gerar_json_edicao()
