from manim import *
import json
import sys

################################################
# 1) CLASSE PARA REPRESENTAR O NÓ DA ÁRVORE
################################################

class TreeNode:
    def __init__(self, node_id, text, children=None):
        self.id = node_id
        self.text = text
        self.children = children if children else []

        # Coordenadas relativas (após a fase de pós-ordem)
        self.x_rel = 0.0
        self.y_rel = 0.0

        # Coordenadas absolutas (após a fase top-down)
        self.x_abs = 0.0
        self.y_abs = 0.0

    def __repr__(self):
        return f"TreeNode(id={self.id}, text={self.text})"

################################################
# 2) FUNÇÃO PARA MONTAR A ÁRVORE A PARTIR DO JSON
################################################

def build_tree_from_json(data):
    """
    Constrói recursivamente a árvore (TreeNode) a partir de
    um dicionário JSON (com chaves: 'id', 'text', 'children', etc.).
    """
    node_id = data.get("id")
    text = data.get("text", "")
    children_data = data.get("children", [])

    children_nodes = [build_tree_from_json(child) for child in children_data]
    return TreeNode(node_id=node_id, text=text, children=children_nodes)

################################################
# 3) ETAPA DE POS-ORDEM PARA CALCULAR LAYOUT
################################################

def compute_layout_postorder(node, sibling_spacing=1.0):
    """
    Visita recursivamente os filhos (pós-ordem), posiciona as subárvores irmãs
    para evitar sobreposições e define x_rel do pai centralizado entre os extremos.

    Retorna: (left_outline, right_outline) = contorno da subárvore
    """
    if not node.children:
        # Nó folha: x_rel = 0, contorno trivial
        node.x_rel = 0.0
        return ({0: 0.0}, {0: 0.0})

    # Recursão nos filhos
    children_contours = []
    for child in node.children:
        l_outline, r_outline = compute_layout_postorder(child, sibling_spacing)
        children_contours.append((child, l_outline, r_outline))

    # Ajustar subárvores da esquerda para a direita
    for i in range(1, len(children_contours)):
        current_child, current_left, current_right = children_contours[i]
        for j in range(i):
            placed_child, placed_left, placed_right = children_contours[j]
            shift = min_distance_to_avoid_overlap(
                placed_child, placed_right,
                current_child, current_left,
                sibling_spacing
            )
            if shift > 0:
                shift_subtree(current_child, shift)

    # Após posicionar os filhos, centraliza o pai:
    leftmost_child = node.children[0]
    rightmost_child = node.children[-1]
    node.x_rel = (leftmost_child.x_rel + rightmost_child.x_rel) / 2.0

    # Constroi o contorno da subárvore e retorna
    left_outline, right_outline = build_outline(node)
    return left_outline, right_outline

def shift_subtree(node, shift_x):
    """ Desloca toda a subárvore enraizada em 'node' no eixo x por shift_x. """
    node.x_rel += shift_x
    for child in node.children:
        shift_subtree(child, shift_x)

def min_distance_to_avoid_overlap(placed_child, placed_right,
                                  current_child, current_left,
                                  sibling_spacing):
    """
    Calcula quanto precisamos deslocar current_child no eixo x
    para não sobrepor placed_child (já posicionado).
    Compara o contorno (right) do placed com o contorno (left) do current.
    """
    max_shift = 0.0
    for depth_left, x_left in current_left.items():
        if depth_left in placed_right:
            overlap = (placed_right[depth_left] + sibling_spacing) - x_left
            if overlap > max_shift:
                max_shift = overlap
    return max_shift

def build_outline(node, depth=0, left_outline=None, right_outline=None):
    """
    Constroi dicionários de contorno para a subárvore:
      - left_outline[depth] = x_min
      - right_outline[depth] = x_max
    """
    if left_outline is None:
        left_outline = {}
    if right_outline is None:
        right_outline = {}

    if depth not in left_outline or node.x_rel < left_outline[depth]:
        left_outline[depth] = node.x_rel
    if depth not in right_outline or node.x_rel > right_outline[depth]:
        right_outline[depth] = node.x_rel

    for child in node.children:
        build_outline(child, depth+1, left_outline, right_outline)

    return left_outline, right_outline

################################################
# 4) ETAPA TOP-DOWN PARA DEFINIR COORDENADAS ABS
################################################

def apply_layout_topdown(node, origin_x=0.0, origin_y=0.0, level_gap=2.0, level=0):
    """
    A partir da raiz, define x_abs e y_abs de cada nó.
    - origin_x, origin_y: coordenadas iniciais da raiz
    - level_gap: espaçamento vertical entre níveis
    - level: nível atual (0 = raiz)
    """
    node.x_abs = origin_x + node.x_rel
    node.y_abs = origin_y - level_gap * level

    for child in node.children:
        apply_layout_topdown(child, node.x_abs, node.y_abs, level_gap, level + 1)

################################################
# 5) MANIM: CRIAR MOBJECTS DOS NÓS E ARESTAS
################################################

def build_manim_objects(node, node_radius=0.2):
    """
    Converte o nó em Mobjects (Dot + Text + Line para edges), retornando
    listas de Mobjects (nós) e (arestas).
    """
    dot = Dot(point=[node.x_abs, node.y_abs, 0], radius=node_radius, color=BLUE)
    text = Text(str(node.text), font_size=24).move_to(
        [node.x_abs, node.y_abs + 0.4, 0]
    )

    node_group = VGroup(dot, text)
    edges = []

    # Arestas para cada filho
    for child in node.children:
        edge = Line(
            start=[node.x_abs, node.y_abs, 0],
            end=[child.x_abs, child.y_abs, 0],
            stroke_width=2
        )
        edges.append(edge)

    # Recursão nos filhos
    child_nodes = []
    child_edges = []
    for child in node.children:
        cn, ce = build_manim_objects(child, node_radius)
        child_nodes.extend(cn)
        child_edges.extend(ce)

    all_nodes = [node_group] + child_nodes
    all_edges = edges + child_edges

    return all_nodes, all_edges

################################################
# 6) CENA MANIM PARA ANIMAR A ÁRVORE
################################################

class TreeScene(Scene):
    def construct(self):
        # Lê parâmetro do arquivo JSON (ex.: "tree_data.json") via sys.argv
        # Se nenhum arquivo for passado, usa "tree_data.json" como padrão.
        json_file = "tree_data.json"
        if len(sys.argv) > 2:
            # Normalmente, sys.argv[-1] é o último parâmetro, mas
            # dependendo de como o Manim é chamado, você pode querer
            # verificar sys.argv após o '--'.
            json_file = sys.argv[-1]

        # 1) Carrega dados do JSON
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 2) Constrói a árvore
        root = build_tree_from_json(data)

        # 3) Faz a etapa de pós-ordem (layout relativo)
        compute_layout_postorder(root, sibling_spacing=1.5)

        # 4) Faz a etapa top-down (coordenadas absolutas), raiz em (0, 3)
        apply_layout_topdown(root, origin_x=0, origin_y=3, level_gap=2.0)

        # 5) Cria Mobjects
        all_nodes, all_edges = build_manim_objects(root, node_radius=0.2)
        nodes_group = VGroup(*all_nodes)
        edges_group = VGroup(*all_edges)

        # 6) Animação simples: aparecer nós e arestas
        # Se quiser criar animação gradual:
        self.play(Create(edges_group), run_time=2)
        self.play(FadeIn(nodes_group), run_time=2)
        self.wait(2)

        # Fim da cena
        self.wait()

################################################
# 7) EXECUÇÃO DO SCRIPT
################################################

# Se quiser rodar diretamente sem manim, você poderia incluir um 'if __name__=="__main__"'
# para testar, mas tipicamente rodamos via:
#   manim -p -ql tree_script.py TreeScene -- dados.json

# Exemplo:
#   manim -p -ql tree_script.py TreeScene -- tree_data.json
