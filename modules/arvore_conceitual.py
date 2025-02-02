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

        
        def create_tree(data, parent_group=None):
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
            
            node = create_node(data, parent_group)
            data["node"] = node
            if data.get("children"):
                for child in data["children"]:
                    child_node = create_tree(child, node)
            return data


        def position_nodes(tree):
            def calculate_width(node):
                if node.get("children"):
                    return sum([calculate_width(child) for child in node["children"]])
                return 1
            
            def position_node(node, x_offset=0.5):
                if node.get("children"):
                    total_width = calculate_width(node)
                    current_x = x_offset - total_width / 2
                    for child in node["children"]:
                        child_width = calculate_width(child)
                        child["node"].next_to(node["node"], DOWN, buff=1).shift(RIGHT * current_x *2)
                        current_x += child_width
                        position_node(child)

            position_node(tree)


        def play_tree(scene, tree, parent_bottom=None):
            if parent_bottom is not None:
                line = CubicBezier(parent_bottom, parent_bottom + DOWN, tree["node"].get_top() + UP, tree["node"].get_top())
#                parent_group.add(line)
                self.play(Create(line))
            scene.play(self.camera.frame.animate.move_to(tree["node"]))
            scene.play(Create(tree["node"]))
            if tree.get("children"):
                parent_bottom = tree["node"].get_bottom()
                for child in tree["children"]:
                    play_tree(scene, child, parent_bottom)
                # Acho um bom local para adicionar as linhas
#                    scene.wait(0.5)

        # Abrir janela do sistema para escolher o arquivo de dados
#        Tk().withdraw()
#        file_path = askopenfilename(title="Selecione o arquivo de dados", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        file_path = "templates/data/história_da_psicologia.json"

        data = get_data(file_path)
        tree = create_tree(data)
        position_nodes(tree)
        play_tree(self, tree)

if __name__ == "__main__":
    # Renderizar a cena
    config.media_width = "75%"
    scene = ArvoreConceitual()
    scene.render()

