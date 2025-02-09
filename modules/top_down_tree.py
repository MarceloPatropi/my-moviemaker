import pandas as pd
import json
from manim import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from typing import Literal
from pydantic import BaseModel

class TreeNode(BaseModel):
    text: str
    shape: Literal["dot", "circle", "rectangle", "ellipse"]
    children: list["TreeNode"]

# Construir a Cena da árvore conceitual
class TopDownTree(MovingCameraScene):
    def __init__(self, data: TreeNode, **kwargs):
        super().__init__(**kwargs)
        self.data = data

    def construct(self):
        def create_tree(data: TreeNode, parent_group=None):
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
                else:
                    group = VGroup(node_shape, node_text).arrange(DOWN)
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
                # return max(1, len(node["text"]) / 10)  # Ajustar largura com base no comprimento do texto
                return 1
            
            def position_node(node, x_offset=0.5):
                if node.get("children"):
                    total_width = calculate_width(node)
                    current_x = x_offset - total_width / 2
                    for child in node["children"]:
                        child_width = calculate_width(child)
                        child["node"].next_to(node["node"], DOWN, buff=1).shift(RIGHT * current_x * 4)
                        current_x += child_width
                        position_node(child)

            position_node(tree)

        def play_tree(scene, tree, parent_bottom=None):
            if parent_bottom is not None:
                line = CubicBezier(parent_bottom, parent_bottom + DOWN, tree["node"].get_top() + UP, tree["node"].get_top())
                scene.play(Create(line), self.camera.frame.animate.move_to(line.get_end()))
            scene.play(self.camera.frame.animate.move_to(tree["node"]))
            scene.play(Create(tree["node"]))
            if tree.get("children"):
                parent_bottom = tree["node"].get_bottom()
                for child in tree["children"]:
                    play_tree(scene, child, parent_bottom)

        tree = create_tree(self.data)
        position_nodes(tree)
        play_tree(self, tree)

if __name__ == "__main__":
    # Renderizar a cena
    config.media_width = "75%"
    root = {
        "id": 1,
        "text": "Root",
        "shape": "circle",
        "children": [
            {
                "id": 2,
                "text": "Child 1",
                "shape": "rectangle",
                "children": [
                    {
                        "id": 4,
                        "text": "Grandchild 1",
                        "shape": "ellipse",
                        "children": []
                    },
                    {
                        "id": 5,
                        "text": "Grandchild 2",
                        "shape": "dot",
                        "children": []
                    }
                ]
            },
            {
                "id": 3,
                "text": "Child 2",
                "shape": "ellipse",
                "children": [
                    {
                        "id": 6,
                        "text": "Grandchild 3",
                        "shape": "circle",
                        "children": []
                    }
                ]
            }
        ]
    }
    scene = TopDownTree(data=root)
    scene.render()

