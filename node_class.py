import csv
from dataclasses import dataclass, field
from typing import Optional, List
import random

@dataclass
class Node:
    name: str
    position_number: int
    bank_number: int = 0
    active: bool = True
    parent_node: Optional[str] = None
    tree_number: int = 0
    title_rank: int = 0
    past_title_rank: int = 0
    paid_point: int = 0
    bonus_point: int = 0
    total_paid_point: int = 0
    total_bonus_point: int = 0
    children: List['Node'] = field(default_factory=list)

    def activate(self) -> None:
        """ノードをアクティブ化し、必要なポイントを支払う"""
        self.paid_point += 20790
        self.total_paid_point += 20790
        self.active = True

    def set_position(self, position: int) -> None:
        """ポジション番号を設定し、必要なポイントを支払う"""
        position_costs = {1: 41580, 3: 82060, 5: 122540, 7: 163020}
        if position in position_costs:
            self.position_number = position
            self.paid_point += position_costs[position]
            self.total_paid_point += position_costs[position]

    def calculate_tree_number(self) -> int:
        """ツリー内のノード総数を計算"""
        count = 1  # 自分自身をカウント
        for child in self.children:
            if child.active:
                count += child.calculate_tree_number()
        return count

    def update_title_rank(self) -> None:
        """タイトルランクを更新"""
        tree_size = self.calculate_tree_number()
        active_children = len([child for child in self.children if child.active])

        rank_conditions = [
            (20, 2, 0), (60, 3, 1), (200, 4, 2),
            (600, 5, 3), (1000, 7, 4), (2000, 10, 5),
            (4000, 10, 6), (6000, 10, 7), (10000, 10, 8),
            (20000, 10, 9)
        ]
        self.past_title_rank = self.title_rank
        self.title_rank = 0
        for tree_req, children_req, rank in rank_conditions:
            if tree_size >= tree_req and active_children >= children_req:
                self.title_rank = rank

    def calculate_bonus1(self) -> int:
        """ボーナス1の計算"""
        tree_size = self.calculate_tree_number() - 1  # 親ノードを除く
        if 4 <= tree_size <= 60:
            return 3000
        elif 64 <= tree_size <= 200:
            return 4000
        elif 204 <= tree_size <= 2000:
            return 5000
        elif 2004 <= tree_size <= 20000:
            return 2000
        return 0

    def calculate_bonus2(self) -> int:
        """ボーナス2の計算"""
        tree_size = self.calculate_tree_number()
        if tree_size == 4:
            return 10000
        elif tree_size == 8:
            return 7000
        elif tree_size == 12:
            return 4000
        elif tree_size == 16:
            return 1000
        return 0

    def calculate_bonus3(self) -> int:
        """ボーナス3の計算"""
        bonus = 0
        for child in self.children:
            if child.active:
                # 子ノードからの15%
                bonus += child.calculate_bonus2() * 0.15
                # 孫ノードからの5%
                for grandchild in child.children:
                    if grandchild.active:
                        bonus += grandchild.calculate_bonus2() * 0.05
                        # ひ孫ノードからの5%
                        for great_grandchild in grandchild.children:
                            if great_grandchild.active:
                                bonus += great_grandchild.calculate_bonus2() * 0.05
        return int(bonus)

    def calculate_bonus4(self) -> int:
        """ボーナス4の計算"""
        if self.title_rank >= 3 and self.past_title_rank >= 3:
            return 100000
        return 0

    def calculate_bonus5(self) -> int:
        """ボーナス5の計算"""
        if self.title_rank >= 4 and self.past_title_rank >= 4:
            return 150000
        return 0

    def calculate_bonus6(self, total_paid_points: int) -> int:
        """ボーナス6の計算"""
        if self.title_rank == 2:
            return int(total_paid_points * 0.01)
        elif self.title_rank >= 3:
            return int(total_paid_points * 0.002)
        return 0

    def arrange_tree(self) -> None:
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

    def _balance_columns(self, columns: List[List['Node']]) -> None:
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
    def save_to_csv(cls, nodes: List['Node'], filename: str) -> None:
        """ノードをCSVファイルに保存"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'name', 'position_number', 'bank_number', 'active',
                'parent_node', 'tree_number', 'title_rank', 'past_title_rank',
                'paid_point', 'bonus_point', 'total_paid_point', 'total_bonus_point'
            ])
            for node in nodes:
                writer.writerow([
                    node.name, node.position_number, node.bank_number,
                    node.active, node.parent_node, node.tree_number,
                    node.title_rank, node.past_title_rank, node.paid_point,
                    node.bonus_point, node.total_paid_point, node.total_bonus_point
                ])

    @classmethod
    def load_from_csv(cls, filename: str) -> List['Node']:
        """CSVファイルからノードを読み込み"""
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
                    total_bonus_point=int(row['total_bonus_point'])
                )
                nodes.append(node)
        return nodes