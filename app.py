import streamlit as st
from node_class import Node
from mlm_core import build_node_hierarchy, calculate_all_bonuses

def main():
    st.title("MLMシミュレーション アプリ")

    st.write("""
    ### フォームで会員数やその他パラメータを入力して、シミュレーションを行います。
    """)

    # 1. フォーム入力を作成 (例として「会員数」「トップノード数」など)
    #    必要に応じて項目を追加・変更してください。
    num_members = st.number_input("会員数を入力してください", min_value=1, max_value=1000, value=5)
    top_layer_nodes = st.number_input("最上位ノードの数", min_value=1, max_value=10, value=1)

    # 2. 実行ボタン
    if st.button("ボーナス計算を実行"):
        # （例）ダミーノードを生成する
        nodes = []
        for i in range(num_members):
            node = Node(
                name=f"Node_{i+1}",
                position_number=1 if i < top_layer_nodes else 3,   # 適当に1 or 3にしてみる
                active=True,
                parent_node=None if i < top_layer_nodes else f"Node_{(i % top_layer_nodes) + 1}"
            )
            nodes.append(node)

        # 親子関係を構築
        root_nodes = build_node_hierarchy(nodes)

        # arrange_tree() や title_rank の更新を行う
        for root in root_nodes:
            root.arrange_tree()

        for node in nodes:
            node.update_title_rank()

        # ボーナス計算
        calculate_all_bonuses(nodes)

        # ▼ CSVには出力せず、画面に表示するだけ ▼
        st.write("### 計算結果一覧")
        # 表にしたいデータをリストにまとめる
        display_data = []
        for node in nodes:
            display_data.append({
                "name": node.name,
                "position_number": node.position_number,
                "paid_point": node.paid_point,
                "bonus_point": node.bonus_point,
                "total_paid_point": node.total_paid_point,
                "total_bonus_point": node.total_bonus_point,
            })

        # 画面にテーブル表示
        st.dataframe(display_data)

        st.success("計算が完了しました。")

if __name__ == "__main__":
    main()
