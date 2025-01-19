import streamlit as st
from node_class import Node
from mlm_core import build_node_hierarchy, calculate_all_bonuses

def create_binary_tree(num_members: int):
    """
    1人目がルート、その後は (i-1)//2 を親にする形で、(ほぼ)二分木を生成。
    """
    nodes = []
    for i in range(num_members):
        if i == 0:
            parent_name = None  # ルートノード
        else:
            parent_index = (i - 1) // 2
            parent_name = f"Node_{parent_index+1}"

        node = Node(
            name=f"Node_{i+1}",
            position_number=1,   # 全員ポジション1とする (必要なら自由に変更可)
            active=True,
            parent_node=parent_name
        )
        nodes.append(node)
    return nodes

def main():
    st.title("MLMシミュレーション（2シーズン分の合計ボーナスを表示）")

    st.write("#### 会員数を入力し、1シーズン目と2シーズン目のボーナス合計を確認します。")

    # 1. フォーム入力：会員数
    num_members = st.number_input(
        "会員数を入力してください", 
        min_value=1, 
        max_value=20000,  # 2万件まで対応
        value=10000
    )

    if st.button("ボーナス計算を実行"):
        # --- 0) ノード作成 ---
        nodes = create_binary_tree(num_members)

        # --- 1シーズン目の計算 ---
        # (1) 親子関係を構築
        root_nodes = build_node_hierarchy(nodes)

        # (2) 全ノードの tree_number を更新
        for node in nodes:
            node.tree_number = node.calculate_tree_number()

        # (3) ツリーを構築 (arrange_tree)
        for root in root_nodes:
            root.arrange_tree()

        # (4) arrange_tree 後にもう一度 tree_number を更新（必要なら）
        for node in nodes:
            node.tree_number = node.calculate_tree_number()

        # (5) タイトルランクを更新
        for node in nodes:
            node.update_title_rank()

        # (6) ボーナスを計算
        calculate_all_bonuses(nodes)

        # 1シーズン目の合計ボーナス
        bonus_season1 = sum(n.bonus_point for n in nodes)

        # --- 2シーズン目の計算 ---
        # ※「2シーズン目も同じノード」が再度 20,790円を支払う想定なら、 activate() を再度呼ぶ
        for node in nodes:
            node.activate()

        # (2') 再度 tree_number を更新
        for node in nodes:
            node.tree_number = node.calculate_tree_number()

        for root in root_nodes:
            root.arrange_tree()

        # arrange_tree 後に再度 tree_number を更新 (必要なら)
        for node in nodes:
            node.tree_number = node.calculate_tree_number()

        for node in nodes:
            node.update_title_rank()

        calculate_all_bonuses(nodes)
        bonus_season2 = sum(n.bonus_point for n in nodes)

        # 1シーズン目 + 2シーズン目 の合計金額
        total_2_seasons = bonus_season1 + bonus_season2

        # --- 結果表示 ---
        st.write(f"**1シーズン目ボーナス合計**: {bonus_season1} 円")
        st.write(f"**2シーズン目ボーナス合計**: {bonus_season2} 円")
        # st.write(f"### **2シーズン分 合計ボーナス**: {total_2_seasons} 円")

        st.success("計算が完了しました！")

if __name__ == "__main__":
    main()
