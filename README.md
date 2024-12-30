# 使い方
テストモード
nodes_create.py
を実行
これで、ノード群を作成します。

そのあと、main.pyを実行

バイナリーの計算、ボーナスの計算、計算結果をcsvで保存する。

# 処理の解説
node_class.pyの中に詰め込んである。
###  変数
    name: str　会員の名前を入れる場所
    position_number: int　ポジション数を入れる場所
    bank_number: int = 0　バンクを入れる場所
    active: bool = True　アクティブか否か
    parent_node: Optional[str] = None　直２の会員からみたら、直１は誰かということ。（始祖会員を調べるときに使う）
    tree_number: int = 0　自分を含む、直１以降全員足したもの
    title_rank: int = 0　タイトル
    past_title_rank: int = 0　一個前のタイトル。title_rankと組み合わせることで、ボーナスの対象かはんだんできる
    paid_point: int = 0　運営が支払うお金
    bonus_point: int = 0　会員が支払うお金
    total_paid_point: int = 0　シーズンごとのトータル
    total_bonus_point: int = 0　シーズン毎のトータル
    children: List['Node'] = field(default_factory=list)　直１のこと（tree_numberを計算するときに使う）
    # 新しい変数を追加
    binary_number_1: int = 0　バイナリーのサイズ（position1の時の）
    binary_number_3: int = 0　バイナリーのサイズ（position3の時の２つ目のバイナリーのサイズ）
    binary_number_5: int = 0　バイナリーのサイズ（position5の時の３つ目のバイナリーのサイズ）
    binary_number_7: int = 0　バイナリーのサイズ（position7の時の４つ目のバイナリーのサイズ）

### メソッド一覧
1. **calculate_binary_numbers(self)**
   - バイナリーの大きさを計算。
2. **activate(self)**
   - ノードをアクティブ化し、必要なポイントを支払う。
3. **set_position(self, position: int)**
   - ポジション番号を設定し、必要なポイントを支払う。
4. **calculate_tree_number(self)**
   - ツリー内のノード総数を計算。
5. **update_title_rank(self)**
   - タイトルランクを更新。
6. **calculate_bonus1(self)**
   - 更新されたボーナス1を計算。
7. **calculate_bonus2(self)**
   - 更新されたボーナス2を計算。
8. **calculate_bonus3(self)**
   - ボーナス3を計算。
9. **calculate_bonus4(self)**
    - ボーナス4を計算。
10. **calculate_bonus5(self)**
    - ボーナス5を計算。
11. **calculate_bonus6(self, total_paid_points: int)**
    - ボーナス6を計算。
12. **arrange_tree(self)**
    - ツリー構造を構築。使ってないっす。
13. **_arrange_position1(self, children: List['Node'])**
    - position_numberが1の場合のツリー構築。使ってないっす。
14. **_arrange_position3(self, children: List['Node'])**
    - position_numberが3の場合のツリー構築。使ってないっす。
15. **_arrange_position5(self, children: List['Node'])**
    - position_numberが5の場合のツリー構築。使ってないっす。
16. **_arrange_position7(self, children: List['Node'])**
    - position_numberが7の場合のツリー構築。使ってないっす。
17. **_balance_columns(self, columns: List[List['Node']])**
    - 列のバランスを取り、bank_numberを更新。使ってないっす。

#### クラスメソッド
1. **save_to_csv(cls, nodes: List['Node'], filename: str)**
   - 更新されたCSV保存機能。
2. **load_from_csv(cls, filename: str)**
   - 更新されたCSV読み込み機能。

