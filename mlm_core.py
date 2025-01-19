from typing import List
from node_class import Node

def build_node_hierarchy(nodes: List[Node]) -> List[Node]:
    """
    ノードの親子関係を構築し、ルートノードのリストを返す
    """
    node_dict = {node.name: node for node in nodes}
    root_nodes = []

    for node in nodes:
        if node.parent_node:
            if node.parent_node in node_dict:
                parent = node_dict[node.parent_node]
                if node not in parent.children:
                    parent.children.append(node)
        else:
            root_nodes.append(node)

    return root_nodes


def calculate_all_bonuses(nodes: List[Node]) -> None:
    """
    全ノードのボーナスを計算
    """
    total_paid_points = sum(node.paid_point for node in nodes)

    for node in nodes:
        if not node.active:
            continue

        # バイナリの数を計算
        node.calculate_binary_numbers()

        # Nodeクラスにある実際のボーナス計算メソッドを呼ぶ
        # (旧: calculate_bonus1,2,3,4,5,6 → 新: calculate_riseup_binary_bonus() 等)
        bonus_riseup   = node.calculate_riseup_binary_bonus()
        bonus_product  = node.calculate_product_free_bonus()
        bonus_matching = node.calculate_matching_bonus()
        bonus_car      = node.calculate_car_bonus()
        bonus_house    = node.calculate_house_bonus()
        bonus_sharing  = node.calculate_sharing_bonus(total_paid_points)

        # 合計ボーナスをセット
        node.bonus_point = (
            bonus_riseup
            + bonus_product
            + bonus_matching
            + bonus_car
            + bonus_house
            + bonus_sharing
        )
        # 累計にも加算
        node.total_bonus_point += node.bonus_point
