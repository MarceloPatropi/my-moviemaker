import pandas as pd
import json
from manim import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Construir a Cena da árvore conceitual
class ArvoreConceitual(MovingCameraScene):
    def construct(self):
        def get_data(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data

        def create_node(node_data, parent_group=None):
            if node_data["shape"] == "circle":
                node_shape = Circle().scale(0.5).set_fill(BLUE, opacity=0.5)
            elif node_data["shape"] == "rectangle":
                node_shape = Square().scale(0.5).set_fill(RED, opacity=0.5)
            elif node_data["shape"] == "ellipse":
                node_shape = Ellipse(width=2.0, height=1.0).set_fill(GREEN, opacity=0.5)
            else:
                node_shape = Dot()
            
            node_text = Text(node_data["text"]).scale(0.5)
            if parent_group is None:
                group = VGroup(node_shape, node_text).arrange(UP)
#                group.move_to(ORIGIN)
            else:
                group = VGroup(node_shape, node_text).arrange(DOWN)
#                group = VGroup(node_shape, node_text).arrange(DOWN).next_to(parent_group, DOWN, buff=1)
            return group
        
        def create_tree(data, parent_group=None):
            node = create_node(data)
            data["node"] = node
            if data.get("children"):
                for child in data["children"]:
                    child_node = create_tree(child, node)
            return data

#            self.add(node)
#            if parent_group is None:
#                group.move_to(ORIGIN)
            #     self.play(Create(group))
#            else:
#                offset = (RIGHT * (index - len(data.get("children", [])) / 2)) * 2  # Aumentar o espaço horizontal
#                group.next_to(parent_group, DOWN, buff=1) #.shift(offset)  # Aumentar o espaço vertical
            #     self.play(Create(group))
            #     # Adicionar linha curva entre o nó pai e o nó filho
#                line = CubicBezier(parent_group.get_bottom(), parent_group.get_bottom() + DOWN, group.get_top() + UP, group.get_top())
#                parent_group.add(line)
            #     self.play(Create(line))
            #     self.play(self.camera.frame.animate.move_to(group))  # Mover a câmera para mostrar o grupo

#            children = data.get("children", [])
#            for i, child in enumerate(children):
#                create_tree(child, node, level + 1, i)
                #node.add(create_tree(child, node, level + 1, i))    # Não é a melhor forma de fazer isso. O Dot e Text da raiz contam como dois MOBs

            # if level not in nodes_at_level:
            #      nodes_at_level[level] = []  # Inicializa a lista para este nível
            # nodes_at_level[level].append(node)
            # level_group = VGroup(*nodes_at_level[level]).arrange(buff=1)
#            self.play(Create(group))
#            return data

        def position_nodes(tree):
            def calculate_width(node):
                if node.get("children"):
                    return sum([calculate_width(child) for child in node["children"]])
                return 1
            
            # width = 0
            # for child in tree["children"]:
            #     width += calculate_width(child)

            def position_node(node, x_offset=0):
                if node.get("children"):
                    x = 0
                    for child in node["children"]:
                        w = calculate_width(child)
                        child["node"].next_to(node["node"], DOWN, buff=1).shift(RIGHT * (x - w / 2) * 2) # Aumentar o espaço horizontal
                        x += w 
                        position_node(child)

            position_node(tree)


        def play_tree(scene, tree):
            scene.play(self.camera.frame.animate.move_to(tree["node"]))
            scene.play(Create(tree["node"]))
            if tree.get("children"):
                for child in tree["children"]:
                    play_tree(scene, child)
                # Acho um bom local para adicionar as linhas
#                    scene.wait(0.5)

        # Abrir janela do sistema para escolher o arquivo de dados
#        Tk().withdraw()
#        file_path = askopenfilename(title="Selecione o arquivo de dados", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        file_path = "templates/data/história_da_psicologia.json"

        data = get_data(file_path)
        tree = create_tree(data)
        position_nodes(tree)
#        create_tree(data)
#        tree.arrange_submobjects(DOWN, buff=1)
#        tree.apply_to_family(lambda mob: mob.arrange_submobjects(DOWN) self.play(FadeIn(mob), self.camera.frame.animate.move_to(mob)))
#        self.add(tree)
#        self.play(Create(self))
        play_tree(self, tree)
#        console.log(sorted(nodes_at_level.items()))
#        console.log(tree)

if __name__ == "__main__":
    # Renderizar a cena
    config.media_width = "75%"
    scene = ArvoreConceitual()
    scene.render()

