import os
import json
from manim import *
from moviepy import *
import base64
import requests

from modules.top_down_tree import TopDownTree, TreeNode
from modules.venn_diagram import VennDiagram
from modules.elevenlabs_tts import ElevenLabsTTS
from modules.pexels_api import PexelsAPI
from modules.openai_chatgpt import OpenAIChatGPT
from modules.pexels_api import PexelsAPI

class VideoWundt(Scene):
    def construct(self):
        # Criar Diagrama de Venn com Filosofia, Teologia e Ciência
        config.output_file = "cena01_venn.mp4"
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

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

if __name__ == "__main__":
    tts = ElevenLabsTTS()
    gpt = OpenAIChatGPT()
    pex = PexelsAPI()

    # scene01_intro = """
    # O que é a alma? Desde a antiguidade, filósofos, teólogos e cientistas tentaram responder essa pergunta. 
    # Para Platão, a alma era imortal. Para Descartes, separada do corpo. Mas no século XIX, Wilhelm Wundt trouxe uma nova abordagem. 
    # A Psicologia experimental transformou o estudo da alma em algo mensurável.
    # """
    # audio = tts.generate_audio(scene01_intro)
    # tts.save_audio(audio, "output/cena01_introdução.mp3")

    print("Gerando animações...")
    # Configurações iniciais
    config.media_dir = "output/"

    # Cena01: Introdução

    config.output_file = "cena01_introdução.mp4"
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
    # venn.render()

    print("Gerando script...")
    # scene01 = VideoFileClip("output/videos/1080p60/cena01_introdução.mp4")
    # frame_t = scene01.duration - 1
    # scene01.save_frame("output/frames/cena01_introdução.png", t=frame_t)
    scene01_image = image_to_base64("output/frames/cena01_introdução.png")
    scene01_prompt = """
    Crie um texto narrativo, usando tom de documentário, para a introdução do vídeo sobre a História da Psicologia.
    A narração deve abordar a questão da alma e a contribuição de Wilhelm Wundt para a Psicologia.
    Utilize a imagem anexa como referência, pois ela será exibida na tela durante a narração.
    Os círculos serão apresentados na tela, um de cada vez, enquanto a narração é feita, seguindo a ordem: Filosofia, Teologia e Ciência.
    A animação continua para apresentar as interseções: Dualismo, Fé vs. Empirismo, Mente racional e termina com a palavra Alma no centro.
    Não mencione diretamente a imagem, pois o espectador estará vendo.
    """

    script_path = "output/scene01_script.txt"
    if os.path.exists(script_path):
        with open(script_path, "r") as f:
            scene01_script = f.read()
    else:
        scene01_script = gpt.generate_response(
            prompt=scene01_prompt,
            image=scene01_image
        )
        with open(script_path, "w") as f:
            f.write(scene01_script)

    # print("Gerando narração...")
    # scene01_narration = tts.generate_audio(scene01_script)
    # tts.save_audio(scene01_narration, "output/scene01_intro.mp3")

    print("Gerando palavaras chave...")
    scene01_keywords_path = "output/scene01_keywords.txt"
    if os.path.exists(scene01_keywords_path):
        with open(scene01_keywords_path, "r") as f:
            scene01_keywords = f.read()
    else:
        scene01_keywords = gpt.generate_response(
            prompt=f"Analise o texto que irei enviar e retorne descrições que ajudem a encontrar imagens e vídeos no Pexels para ilustrar a narração. Separe as descrições com ';'. Narração: {scene01_script}"
        )
        with open(scene01_keywords_path, "w") as f:
            f.write(scene01_keywords)

    # print("Buscando imagens e vídeos no Pexels...")
    # keywords = scene01_keywords.split(';')
    # for keyword in keywords:
    #     keyword = keyword.strip()
    #     if keyword:
    #         print(f"Buscando mídia para: {keyword}")
    #         imagens = pex.search_photos(keyword, per_page=3)
    #         videos = pex.search_videos(keyword, per_page=3)

    #         os.makedirs("output/pexels/imagens", exist_ok=True)
    #         os.makedirs("output/pexels/videos", exist_ok=True)

    #         for i, img in enumerate(imagens["photos"]):
    #             img_url = img["src"]["original"]
    #             img_data = requests.get(img_url).content
    #             img_name = os.path.join("output/pexels/imagens", f"{keyword}_img_{i}.jpg")
    #             with open(img_name, 'wb') as handler:
    #                 handler.write(img_data)

    #         for i, vid in enumerate(videos["videos"]):
    #             vid_url = vid["video_files"][0]["link"]
    #             vid_data = requests.get(vid_url).content
    #             vid_name = os.path.join("output/pexels/videos", f"{keyword}_vid_{i}.mp4")
    #             with open(vid_name, 'wb') as handler:
    #                 handler.write(vid_data)
#    buscar_midias()

    # Cena 02
    print("Cena 02 ...")
    config.output_file = "cena02_árvore.mp4"

    scene02_prompt = """
    Crie a estrutura de uma árvore conceitual, começando pela raiz Alma e gerando quantos filhos forem necessários para contar a história da psicologia moderna.
    Siga a lógica de evolução do conhecimento sobre a Alma ou Psique. 
    Comece na Antiguidade, com as primeiras trepanações, passando pelo egito e oriente, chegando na Grécia e avançando pelas idades média e moderna.
    Cite conceitos importantes e pensadores.
    """
    scene02_tree_path = "output/scene02_tree.json"
    if os.path.exists(scene02_tree_path):
        with open(scene02_tree_path, "r") as f:
            scene02_tree = json.load(f)
    else:
        scene02_tree = json.loads( 
            gpt.generate_response(
                prompt=scene02_prompt,
                response_format=TreeNode
            )
        )

        with open(scene02_tree_path, "w") as f:
            json.dump(scene02_tree, f, indent=4)
    tree = TopDownTree(scene02_tree)
    tree.render()

    print("Criando JSON para edição no Premiere...")
#    gerar_json_edicao()
