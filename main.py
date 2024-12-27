import time
from typing import List
from node_class import Node

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

def calculate_all_bonuses(nodes: List[Node]) -> None:
    """全ノードのボーナスを計算"""
    # 全ノードの支払いポイントの合計を計算
    total_paid_points = sum(node.paid_point for node in nodes)

    for node in nodes:
        if not node.active:
            continue

        # ボーナス1-5の計算
        bonus1 = node.calculate_bonus1()
        bonus2 = node.calculate_bonus2()
        bonus3 = node.calculate_bonus3()
        bonus4 = node.calculate_bonus4()
        bonus5 = node.calculate_bonus5()
        
        # ボーナス6の計算
        bonus6 = node.calculate_bonus6(total_paid_points)

        # 合計ボーナスの設定
        node.bonus_point = bonus1 + bonus2 + bonus3 + bonus4 + bonus5 + bonus6
        node.total_bonus_point += node.bonus_point

def save_results(nodes: List[Node], iteration: int) -> None:
    """結果をCSVファイルに保存"""
    # ノードの状態を保存
    node_filename = f"{iteration}_nodes.csv"
    Node.save_to_csv(nodes, node_filename)

    # ポイントサマリーを保存
    point_filename = f"{iteration}_points.csv"
    total_paid = sum(node.paid_point for node in nodes)
    total_bonus = sum(node.bonus_point for node in nodes)
    total_paid_all = sum(node.total_paid_point for node in nodes)
    total_bonus_all = sum(node.total_bonus_point for node in nodes)

    with open(point_filename, 'w') as f:
        f.write("metric,current_season,all_seasons\n")
        f.write(f"total_paid,{total_paid},{total_paid_all}\n")
        f.write(f"total_bonus,{total_bonus},{total_bonus_all}\n")

def main():
    # シミュレーションのパラメータ
    num_simulations = 3  # シミュレーション回数

    for sim in range(num_simulations):
        print(f"Starting simulation {sim + 1}")
        
        if sim == 0:
            csv_name = "nodes.csv"
        else:
            csv_name = str(timestamp) + "_nodes.csv"
        # 1. CSVからノードを読み込む
        nodes = Node.load_from_csv(csv_name)
        
        # 2. ノードの階層構造を構築
        root_nodes = build_node_hierarchy(nodes)
        
        # 3. 各ルートノードからツリーを構築
        for root in root_nodes:
            root.arrange_tree()
            
        # 4. タイトルランクを更新
        for node in nodes:
            node.update_title_rank()
            
        # 5. ボーナスを計算
        calculate_all_bonuses(nodes)
        
        # 6. 結果を保存
        timestamp = int(time.time())
        save_results(nodes, timestamp)
        
        print(f"Simulation {sim + 1} completed")
        time.sleep(1)

if __name__ == "__main__":
    main()