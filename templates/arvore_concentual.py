import pandas as pd
from manim import *

# Construir a Cena da árvore conceitual
class ArvoreConceitual(Scene):
    def construct(self):
        def get_data(file_path):
            data = pd.read_csv(file_path, sep="|", skiprows=1, usecols=[1, 2, 3, 4])

            # Renomear colunas e limpar espaços extras
            data.columns = ["id", "text", "shape", "parent"]
            data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

            # Converter tipos de colunas
            for column in data.columns:
                try:
                    # Tentar converter para numérico
                    data[column] = pd.to_numeric(data[column])
                    # Verificar se a coluna pode ser convertida para inteiro
                    if pd.api.types.is_float_dtype(data[column]):
                        if data[column].dropna().apply(float.is_integer).all():
                            data[column] = data[column].astype('Int64')
                except ValueError:
                    # Se a conversão falhar, manter os valores originais
                    data[column] = data[column].astype(str)

            # Adicionar coluna para armazenar os nós
            data["node"] = None

            # Criar os nós
            for _, node in data.iterrows():
                if node["shape"] == "circle":
                    node_shape = Circle().scale(0.5).set_fill(BLUE, opacity=0.5)
                elif node["shape"] == "rectangle":
                    node_shape = Square().scale(0.5).set_fill(RED, opacity=0.5)
                elif node["shape"] == "ellipse":
                    node_shape = Ellipse(width=2.0, height=1.0).set_fill(GREEN, opacity=0.5)
                else:
                    node_shape = Dot()
                
                node_text = Text(node["text"]).scale(0.5)
                group = VGroup(node_shape, node_text).arrange(UP)

                if pd.isna(node["parent"]):
                    group.move_to(ORIGIN)
                    data.at[node.name, "node"] = group
                else:
                    parent_node = data.loc[data["id"] == node["parent"]].iloc[0]
                    if parent_node is not None:
                        n_sibilings = len(data.loc[data["parent"] == parent_node["id"]])
                        offset = (RIGHT * (node.name - len(data.loc[data["parent"] == parent_node["id"]]) / 2)) * 1.5
                        group.next_to(parent_node["node"], DOWN, buff=1).shift(offset)
                        data.at[node.name, "node"] = group

            return data

        def create_tree(data):
            raiz = data.loc[data["parent"].isna()].iloc[0]
            raiz["node"].move_to(ORIGIN)
            self.play(Create(raiz["node"]))
            create_children(raiz)

        def create_children(raiz, level=0):        
            children = data.loc[data["parent"] == raiz["id"]]
            if not children.empty:
                level += 1
                index = 0.5
                for _, node in children.iterrows():
                    group = node["node"]
                    offset = (RIGHT * (index - len(children) / 2)) * 2
                    group.next_to(raiz["node"], DOWN, buff=1).shift(offset)
                    self.play(Create(group))
                    index += 1
                    # Adicionar linha curva entre o nó pai e o nó filho
                    line = CubicBezier(raiz["node"].get_bottom(), raiz["node"].get_bottom() + DOWN, group.get_top() + UP, group.get_top())
                    self.play(Create(line))
                    create_children(node, level)
    
        file_path = "/home/patropi/my-moviemaker/scenes/arvore_conceitual.md"
        data = get_data(file_path)

        create_tree(data)

