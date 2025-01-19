import random
from typing import List, Dict
from node_class import Node

def create_random_nodes(num_layers: List[int]) -> List[Node]:
    """
    ランダムなノード群を作成
    num_layers: 各層のノード数のリスト [第1層のノード数, 第2層の各ノードの子ノード数, ...]
    """
    nodes = []
    node_counter = 1
    layer_nodes: Dict[int, List[Node]] = {0: []}  # 各層のノードを保持

    # 第1層（ルートノード）の作成
    for _ in range(num_layers[0]):
        node = Node(
            name=f"Node_{node_counter}",
            position_number=random.choice([1, 3, 5, 7]),
            active=True
        )
        nodes.append(node)
        layer_nodes[0].append(node)
        node_counter += 1

    # 第2層以降の作成
    for layer, num_children in enumerate(num_layers[1:], 1):
        layer_nodes[layer] = []
        for parent in layer_nodes[layer-1]:
            for _ in range(num_children):
                node = Node(
                    name=f"Node_{node_counter}",
                    position_number=random.choice([1, 3, 5, 7]),
                    parent_node=parent.name,
                    active=random.random() > 0.1  # 90%の確率でアクティブ
                )
                nodes.append(node)
                layer_nodes[layer].append(node)
                parent.children.append(node)
                node_counter += 1

    return nodes

def build_node_hierarchy(nodes: List[Node]) -> List[Node]:
    """ノードの親子関係を構築し、ルートノードのリストを返す"""
    # ノードをname->nodeの辞書に変換
    node_dict = {node.name: node for node in nodes}
    root_nodes = []

    # 親子関係を構築
    for node in nodes:
        if node.parent_node:
            if node.parent_node in node_dict:
                parent = node_dict[node.parent_node]
                if node not in parent.children:
                    parent.children.append(node)
        else:
            root_nodes.append(node)

    return root_nodes

def update_tree_numbers(node: Node) -> None:
    """ツリー番号を再帰的に更新"""
    node.tree_number = node.calculate_tree_number()
    for child in node.children:
        if child.active:
            update_tree_numbers(child)

if __name__ == "__main__":
    # 設定パラメータ
    layer_config = [1, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]  # 各層のノード数設定

    # 1. ランダムなノード群を作成
    nodes = create_random_nodes(layer_config)
    
    # 2. ノードの階層構造を構築
    root_nodes = build_node_hierarchy(nodes)
    
    # 3. ツリー番号を更新
    for root in root_nodes:
        update_tree_numbers(root)
    
    #4. アクティブなノードのみバイナリーのサイズを計算する。
    for node in nodes:
        if not node.active:
            continue

        node.calculate_binary_numbers()
    
    # 5. CSVファイルに保存
    Node.save_to_csv(nodes, "nodes.csv")
    
    print("Nodes created and saved to nodes.csv")
