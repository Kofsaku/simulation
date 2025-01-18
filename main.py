import time
from typing import List, Dict, Tuple
from node_class import Node

def build_node_hierarchy(nodes: List[Node]) -> List[Node]:
    """ノードの親子関係を構築し、ルートノードのリストを返す"""
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

def calculate_all_bonuses(nodes: List[Node]) -> Dict[str, Tuple[int, int]]:
    """全ノードのボーナスを計算し、種類別の合計金額と発生件数を返す"""
    # 全ノードの支払いポイントの合計を計算
    total_paid_points = sum(node.paid_point for node in nodes)

    # ボーナス集計用の辞書を初期化
    bonus_summary = {
        'riseup_binary_bonus': [0, 0],  # [合計金額, 発生件数]
        'product_free_bonus': [0, 0],
        'matching_bonus': [0, 0],
        'car_bonus': [0, 0],
        'house_bonus': [0, 0],
        'sharing_bonus': [0, 0]
    }

    for node in nodes:
        if not node.active:
            continue

        # binary numbersの計算
        node.calculate_binary_numbers()

        # 各ボーナスの計算と集計
        bonuses = {
            'riseup_binary_bonus': node.calculate_riseup_binary_bonus(),
            'product_free_bonus': node.calculate_product_free_bonus(),
            'matching_bonus': node.calculate_matching_bonus(),
            'car_bonus': node.calculate_car_bonus(),
            'house_bonus': node.calculate_house_bonus(),
            'sharing_bonus': node.calculate_sharing_bonus(total_paid_points)
        }

        # ボーナスの集計
        for bonus_type, amount in bonuses.items():
            if amount > 0:
                bonus_summary[bonus_type][0] += amount  # 金額を加算
                bonus_summary[bonus_type][1] += 1      # 件数を加算

        # 合計ボーナスの設定
        node.bonus_point = sum(bonuses.values())
        node.total_bonus_point += node.bonus_point

    return bonus_summary

def save_results(nodes: List[Node], bonus_summary: Dict[str, Tuple[int, int]], iteration: int) -> None:
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
        f.write("metric,amount,count\n")
        f.write(f"total_paid,{total_paid},N/A\n")
        
        # 各ボーナスの詳細を書き出し
        for bonus_type, (amount, count) in bonus_summary.items():
            f.write(f"{bonus_type},{amount},{count}\n")
        
        f.write(f"total_bonus,{total_bonus},N/A\n")
        f.write(f"\nall_seasons_total_paid,{total_paid_all},N/A\n")
        f.write(f"all_seasons_total_bonus,{total_bonus_all},N/A\n")

def main():
    # シミュレーションのパラメータ
    num_simulations = 1  # シミュレーション回数

    for sim in range(num_simulations):
        print(f"Starting simulation {sim + 1}")
        
        # 1. CSVからノードを読み込む
        nodes = Node.load_from_csv("nodes.csv")
        
        # 2. ノードの階層構造を構築
        root_nodes = build_node_hierarchy(nodes)
        
        # 3. 各ルートノードからツリーを構築
        for root in root_nodes:
            root.arrange_tree()
            
        # 4. タイトルランクを更新
        for node in nodes:
            node.update_title_rank()
            
        # 5. ボーナスを計算し、サマリーを取得
        bonus_summary = calculate_all_bonuses(nodes)
        
        # 6. 全てのノードをアクティブにする
        for node in nodes:
            node.activate()
        
        # 7. 結果を保存
        timestamp = int(time.time())
        save_results(nodes, bonus_summary, timestamp)
        
        print(f"Simulation {sim + 1} completed")
        time.sleep(1)

if __name__ == "__main__":
    main()
