from dataclasses import dataclass, field
from typing import Optional, List
import csv

@dataclass
class Node:
    name: str #会員の名前。入力必須。
    position_number: int #ポジション数。入力必須。
    bank_number: int = 0 #バンクを何個持ってるか。
    active: bool = True #アクティブか否か。入力必須。
    parent_node: Optional[str] = None #誰に紹介されたか。入力必須。
    tree_number: int = 0 #自分を含め、直１以下に何人いるか。人数。
    title_rank: int = 0 #現在のタイトルは何か
    past_title_rank: int = 0 #一個前のタイトルは何か
    paid_point: int = 0 #会員が支払った金額、つまり売り上げ。現在は固定で20,790円支払うように設定している。入力必須。
    bonus_point: int = 0 #ボーナスの金額。ボーナス計算の時に使う。
    total_paid_point: int = 0 #売り上げ合計
    total_bonus_point: int = 0 #ボーナス合計
    children: List['Node'] = field(default_factory=list) #直１のリスト
    # 新しい変数を追加
    binary_number_1: int = 0 #ポジション１の時のバイナリーのサイズ。
    binary_number_3: int = 0 #ポジション３の時の２個目のバイナリーのサイズ。
    binary_number_5: int = 0 #ポジション５の時の３個目のバイナリーのサイズ。
    binary_number_7: int = 0 #ポジション７の時の４個目のバイナリーのサイズ。

    def process_bank_number(self, node1: 'Node', node2: 'Node') -> None: #バンクナンバーを足したり引いたりするメソッド
        """bank_number処理を実行"""
        if not node1 or not node2:
            return
            
        tree1 = node1.tree_number
        tree2 = node2.tree_number
        
        #tree1とtree2は右側と左側を指しています。
        
        if tree1 != tree2: #右側と左側の数が違うとき、バンクナンバーを使って、バイナリーのサイズを大きくする。
            # bank_numberを使って tree_number を調整
            while self.bank_number > 0 and tree2 < tree1: #バンクナンバーが１か２の時に大きさを調整する。
                tree2 += 1
                self.bank_number -= 1 #大きさを調整したら、バンクナンバーを１減らす
                
            # 差分をbank_numberに貯蔵（最大2まで）
            diff = min(tree1 - tree2, 2) #右側と左側の二つの差を計算し、バンクナンバーに
            if diff > 0:
                self.bank_number = min(self.bank_number + diff, 2)

    def calculate_binary_numbers(self) -> None: #ポジション数に応じてバイナリーのサイズを計算する。
        """バイナリーの大きさを計算"""
        active_children = sorted(
            [child for child in self.children if child.active],
            key=lambda x: x.tree_number,
            reverse=True
        )
        #まずは、直１を会員のtree_number数に応じてソートする。
        if not active_children:
            return

        if self.position_number >= 1 and len(active_children) >= 2: #一番大きい直１会員と二番目に大きい直２会員をとってきて、バンクナンバー処理して、バイナリーのサイズを計算する。
            node1, node2 = active_children[0:2]
            self.binary_number_1 = (min(node1.tree_number, node2.tree_number) - 1) * 2
            self.process_bank_number(node1, node2)

        if self.position_number >= 3 and len(active_children) >= 4:
            node3, node4 = active_children[2:4]
            self.binary_number_3 = (min(node3.tree_number, node4.tree_number) - 1) * 2
            self.process_bank_number(node3, node4)

        if self.position_number >= 5 and len(active_children) >= 6:
            node5, node6 = active_children[4:6]
            self.binary_number_5 = (min(node5.tree_number, node6.tree_number) - 1) * 2
            self.process_bank_number(node5, node6)

        if self.position_number >= 7 and len(active_children) >= 8:
            node7, node8 = active_children[6:8]
            self.binary_number_7 = (min(node7.tree_number, node8.tree_number) - 1) * 2
            self.process_bank_number(node7, node8)

    def activate(self) -> None: #会員をアクティブにするメソッド。定額で20,790円支払うことにしている。支払額は手動入力ですね。
        """ノードをアクティブ化し、必要なポイントを支払う"""
        self.paid_point += 20790
        self.total_paid_point += 20790
        self.active = True

    def set_position(self, position: int) -> None: #ポジション数に応じて、会員が支払っているであろう金額を自動で計算する。まあ本番環境は使わないでしょう。
        """ポジション番号を設定し、必要なポイントを支払う"""
        position_costs = {1: 41580, 3: 82060, 5: 122540, 7: 163020}
        if position in position_costs:
            self.position_number = position
            self.paid_point += position_costs[position]
            self.total_paid_point += position_costs[position]

    def calculate_tree_number(self) -> int: #自分自身以下の会員が何人いるか計算する。tree_numberと名付けている。
        """ツリー内のノード総数を計算"""
        count = 1  # 自分自身をカウント
        for child in self.children:
            if child.active:
                count += child.calculate_tree_number()
        return count

    def update_title_rank(self) -> None: #タイトルランクを自動で更新するメソッド。現在のランクをpast_title_rankに入れてから、title_rankを更新する。
        """タイトルランクを更新"""
        tree_size = self.calculate_tree_number()
        active_children = len([child for child in self.children if child.active])

        rank_conditions = [
            (20, 2, 1), (60, 3, 2), (200, 4, 3),
            (600, 5, 4), (1000, 7, 5), (2000, 10, 6),
            (4000, 10, 7), (6000, 10, 8), (10000, 10, 9),
            (20000, 10, 10)
        ] #一番右の数字がタイトルランクを示している。左がtree_number、真ん中が直1。タイトルの条件値になっている。
        self.past_title_rank = self.title_rank
        self.title_rank = 0
        for tree_req, children_req, rank in rank_conditions:
            if tree_size >= tree_req and active_children >= children_req:
                self.title_rank = rank

    def calculate_riseup_binary_bonus(self) -> int: #ライズアップボーナスを計算する。バイナリーナンバーを使います。
        """更新されたバイナリーボーナスの計算"""
        def calculate_bonus_for_binary(binary_number: int) -> float:
            if 4 <= binary_number <= 60:
                return 3000 * binary_number / 4
            elif 64 <= binary_number <= 200:
                return 3000 * 15 + 4000 * (binary_number - 60) / 4
            elif 204 <= binary_number <= 2000:
                return 3000 * 15 + 4000 * 35 + 5000 * (binary_number - 200) / 4
            elif 2004 <= binary_number <= 20000:
                return 3000 * 15 + 4000 * 35 + 5000 * 450 + 2000 * (binary_number - 2000) / 4
            elif binary_number > 20000:
                return 3000 * 15 + 4000 * 35 + 5000 * 450 + 2000 * 4500
            return 0

        bonus = 0 #ポジション数に応じて計算する。position_numberが増えると何度もボーナスが加算される。
        if self.position_number >= 1:
            bonus += calculate_bonus_for_binary(self.binary_number_1)
        if self.position_number >= 3:
            bonus += calculate_bonus_for_binary(self.binary_number_3)
        if self.position_number >= 5:
            bonus += calculate_bonus_for_binary(self.binary_number_5)
        if self.position_number >= 7:
            bonus += calculate_bonus_for_binary(self.binary_number_7)
            
        return int(bonus)

    def calculate_product_free_bonus(self) -> int: #プロダクトフリーボーナスを計算する。
        """更新された製品無料ボーナスの計算"""
        def calculate_bonus_for_binary(binary_number: int) -> int:
            if binary_number == 4:
                return 10000
            elif binary_number == 8:
                return 7000
            elif binary_number == 12:
                return 4000
            elif binary_number == 16:
                return 1000
            return 0

        bonus = 0 #ポジション数に応じて計算する。position_numberが増えると何度もボーナスが加算される。
        if self.position_number >= 1:
            bonus += calculate_bonus_for_binary(self.binary_number_1)
        if self.position_number >= 3:
            bonus += calculate_bonus_for_binary(self.binary_number_3)
        if self.position_number >= 5:
            bonus += calculate_bonus_for_binary(self.binary_number_5)
        if self.position_number >= 7:
            bonus += calculate_bonus_for_binary(self.binary_number_7)
            
        return bonus

    def calculate_matching_bonus(self) -> int: #マッチングボーナスの計算。
        """マッチングボーナスの計算"""
        bonus = 0
        for child in self.children:
            if child.active:
                # 子ノードからの15%
                bonus += child.calculate_product_free_bonus() * 0.15
                # 孫ノードからの5%
                for grandchild in child.children:
                    if grandchild.active:
                        bonus += grandchild.calculate_product_free_bonus() * 0.05
                        # ひ孫ノードからの5%
                        for great_grandchild in grandchild.children:
                            if great_grandchild.active:
                                bonus += great_grandchild.calculate_product_free_bonus() * 0.05
        return int(bonus)

    def calculate_car_bonus(self) -> int: #カーボーナスの計算。title_rankとpast_title_rankを使う。今回は条件を満たしていれば、満額もらえるようにしている。
        """車ボーナスの計算"""
        if self.title_rank >= 4 and self.past_title_rank >= 4:
            return 100000
        return 0

    def calculate_house_bonus(self) -> int: #ハウスボーナスの計算。title_rankとpast_title_rankを使う。今回は条件を満たしていれば、満額もらえるようにしている。
        """住宅ボーナスの計算"""
        if self.title_rank >= 5 and self.past_title_rank >= 5:
            return 150000
        return 0

    def calculate_sharing_bonus(self, total_paid_points: int) -> int: #シェアリングボーナスの計算。
        """シェアリングボーナスの計算"""
        if self.title_rank == 3:
            return int(total_paid_points * 0.01)
        elif self.title_rank >= 4:
            return int(total_paid_points * 0.002)
        return 0

    def arrange_tree(self) -> None: #ポジション数に応じてバイナリーを作るメソッド。
        """ツリー構造を構築"""
        if not self.active:
            return

        # 子ノードを孫ノード以下の数でソート
        active_children = [child for child in self.children if child.active]
        active_children.sort(key=lambda x: x.calculate_tree_number(), reverse=True)

        # position_numberに応じてツリーを構築
        if self.position_number == 1:
            self._arrange_position1(active_children)
        elif self.position_number == 3:
            self._arrange_position3(active_children)
        elif self.position_number == 5:
            self._arrange_position5(active_children)
        elif self.position_number == 7:
            self._arrange_position7(active_children)

    def _arrange_position1(self, children: List['Node']) -> None:
        """position_number 1のツリー構築"""
        if len(children) < 2:
            return
        
        # 最大2つの列を作成
        columns = [children[0:1], children[1:2]]
        self._balance_columns(columns)

    def _arrange_position3(self, children: List['Node']) -> None:
        """position_number 3のツリー構築"""
        if len(children) < 4:
            return
        
        # 4つの列を作成
        columns = [
            children[0:1], children[1:2],
            children[2:3], children[3:4]
        ]
        self._balance_columns(columns)

    def _arrange_position5(self, children: List['Node']) -> None:
        """position_number 5のツリー構築"""
        if len(children) < 6:
            return
        
        # 6つの列を作成
        columns = [
            children[0:1], children[1:2],
            children[2:3], children[3:4],
            children[4:5], children[5:6]
        ]
        self._balance_columns(columns)

    def _arrange_position7(self, children: List['Node']) -> None:
        """position_number 7のツリー構築"""
        if len(children) < 8:
            return
        
        # 8つの列を作成
        columns = [
            children[0:1], children[1:2],
            children[2:3], children[3:4],
            children[4:5], children[5:6],
            children[6:7], children[7:8]
        ]
        self._balance_columns(columns)

    def _balance_columns(self, columns: List[List['Node']]) -> None: #binary_numberを導入する前に作ったやつ。
        """列のバランスを取り、bank_numberを更新"""
        # 列の数を計算
        column_sizes = [len(col) for col in columns]
        min_size = min(column_sizes)
        max_size = max(column_sizes)
        
        # bank_numberの使用
        if self.bank_number > 0:
            for i in range(len(columns)):
                if column_sizes[i] < max_size:
                    if self.bank_number > 0:
                        column_sizes[i] += 1
                        self.bank_number -= 1

        # 差分を計算し、bank_numberを更新
        total_diff = 0
        for i in range(len(columns)):
            if column_sizes[i] > min_size:
                diff = column_sizes[i] - min_size
                total_diff += diff
                column_sizes[i] = min_size

        # 最大2個までbank_numberに加算
        self.bank_number = min(self.bank_number + total_diff, 2)

    @classmethod
    def save_to_csv(cls, nodes: List['Node'], filename: str) -> None: #ＣＳＶに保存するメソッド。
        """更新されたCSV保存機能"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'name', 'position_number', 'bank_number', 'active',
                'parent_node', 'tree_number', 'title_rank', 'past_title_rank',
                'paid_point', 'bonus_point', 'total_paid_point', 'total_bonus_point',
                'binary_number_1', 'binary_number_3', 'binary_number_5', 'binary_number_7',
                'riseup_binary_bonus', 'product_free_bonus', 'matching_bonus',
                'car_bonus', 'house_bonus', 'sharing_bonus'
            ])
            
            total_paid_points = sum(node.paid_point for node in nodes)
            
            for node in nodes:
                # 各ボーナスを計算
                riseup_binary_bonus = node.calculate_riseup_binary_bonus()
                product_free_bonus = node.calculate_product_free_bonus()
                matching_bonus = node.calculate_matching_bonus()
                car_bonus = node.calculate_car_bonus()
                house_bonus = node.calculate_house_bonus()
                sharing_bonus = node.calculate_sharing_bonus(total_paid_points)
                
                writer.writerow([
                    node.name, node.position_number, node.bank_number,
                    node.active, node.parent_node, node.tree_number,
                    node.title_rank, node.past_title_rank, node.paid_point,
                    node.bonus_point, node.total_paid_point, node.total_bonus_point,
                    node.binary_number_1, node.binary_number_3, node.binary_number_5,
                    node.binary_number_7,
                    riseup_binary_bonus, product_free_bonus, matching_bonus,
                    car_bonus, house_bonus, sharing_bonus
                ])

    @classmethod
    def load_from_csv(cls, filename: str) -> List['Node']: #ＣＳＶを読み込むメソッド。
        """更新されたCSV読み込み機能"""
        nodes = []
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                node = cls(
                    name=row['name'],
                    position_number=int(row['position_number']),
                    bank_number=int(row['bank_number']),
                    active=row['active'].lower() == 'true',
                    parent_node=row['parent_node'] if row['parent_node'] else None,
                    tree_number=int(row['tree_number']),
                    title_rank=int(row['title_rank']),
                    past_title_rank=int(row['past_title_rank']),
                    paid_point=int(row['paid_point']),
                    bonus_point=int(row['bonus_point']),
                    total_paid_point=int(row['total_paid_point']),
                    total_bonus_point=int(row['total_bonus_point']),
                    binary_number_1=int(row['binary_number_1']),
                    binary_number_3=int(row['binary_number_3']),
                    binary_number_5=int(row['binary_number_5']),
                    binary_number_7=int(row['binary_number_7'])
                )
                nodes.append(node)
        return nodes
