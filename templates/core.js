import json
from manim import *

# Importar classes de cenas
from moviemaker.scenes.arvore_conceitual import ArvoreConceitual
from moviemaker.scenes.linha_do_tempo import LinhaDoTempo
from moviemaker.scenes.citacao import Citacao

def load_json(json_file):
    """
    Carrega o arquivo JSON e retorna os dados.
    """
    with open(json_file, 'r') as f:
        return json.load(f)

def render_scene(data):
    """
    Renderiza a cena com base no tipo especificado no JSON.
    """
    scene_type = data.get("type")
    if scene_type == "ArvoreConceitual":
        scene = ArvoreConceitual(data)
    elif scene_type == "LinhaDoTempo":
        scene = LinhaDoTempo(data)
    elif scene_type == "Citacao":
        scene = Citacao(data)
    else:
        raise ValueError(f"Tipo de cena desconhecido: {scene_type}")
    
    # Renderizar a cena
    config.media_dir = "media/videos"
    scene.render()

if __name__ == "__main__":
    # Carregar JSON de exemplo
    data = load_json("moviemaker/templates/exemplo_arvore.json")
    render_scene(data)
