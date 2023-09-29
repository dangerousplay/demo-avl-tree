from typing import Optional, Any
import networkx as nx
import uuid


class Node:

    def __init__(self, value, left=None, right=None, nid=None):
        self.left = left
        self.right = right
        self.value = value
        self.id = nid if nid else uuid.uuid4()
        self.height = 1
        self.balance = 0

        self.__update_weight_balance__()

    def insert(self, value):
        if value >= self.value:
            if not self.right:
                self.right = Node(value)
            else:
                self.right = self.right.insert(value)
        else:
            if not self.left:
                self.left = Node(value)
            else:
                self.left = self.left.insert(value)

        self.__update_weight_balance__()

        if self.balance > 1:
            if value < self.left.value:
                return self.__rotate_right__()
            else:
                return self.__rotate_left_right__()
        elif self.balance < -1:
            if value > self.right.value:
                return self.__rotate_left__()
            else:
                return self.__rotate_right_left__()

        return self

    def delete(self, value):
        if self.right:
            rvalue = self.right.value

            if value == rvalue:
                return self.right.delete(value)

            if value > self.value:
                return self.right.delete(value)

        if self.left:
            lvalue = self.left.value

            if value == lvalue:
                pass

            if value < self.value:
                return self.left.delete(value)

        return self

    def __contains__(self, item):
        if self.right and item > self.value:
            return self.right.__contains__(item)

        if self.left and item < self.value:
            return self.left.__contains__(item)

        return self.value == item

    def __update_weight_balance__(self):
        self.__update_height__()
        self.balance = self.__balance__()

    def __rotate_right_left__(self):
        self.right = self.right.__rotate_right__()

        return self.__rotate_left__()

    def __rotate_left_right__(self):
        self.left = self.left.__rotate_left__()
        return self.__rotate_right__()

    def __rotate_right__(self):
        x = self.left
        y = x.right

        x.right = self
        self.left = y

        self.__update_weight_balance__()
        x.__update_weight_balance__()

        return x

    def __rotate_left__(self):
        x = self.right
        y = x.left

        x.left = self
        self.right = y

        self.__update_weight_balance__()
        x.__update_weight_balance__()

        return x

    def __update_height__(self):
        self.height = 1 + max(Node.height(self.left), Node.height(self.right))

    def __balance__(self):
        return Node.height(self.left) - Node.height(self.right)

    def max_value(self):
        compare = [self]

        if self.right:
            compare.append(self.right.max_value())

        if self.left:
            compare.append(self.left.max_value())

        return max(compare)

    def min_value(self):
        compare = [self]

        if self.right:
            compare.append(self.right.min_value())

        if self.left:
            compare.append(self.left.min_value())

        return min(compare)

    def __le__(self, other):
        return self.value <= other.value

    def __lt__(self, other):
        return self.value < other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __str__(self):
        return f"[v={self.value} l={self.left} r={self.right}]"

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        length = 1

        if self.right:
            length += self.right.__len__()

        if self.left:
            length += self.left.__len__()

        return length

    @staticmethod
    def height(node) -> int:
        if node:
            return node.height
        else:
            return 0


class AVLTree:
    node: Optional[Node]

    def __init__(self):
        self.node = None

    def insert(self, value):
        if not self.node:
            self.node = Node(value)
        else:
            self.node = self.node.insert(value)

    def __len__(self):
        return self.node.__len__()

    def __str__(self):
        return f"AVL [{self.node}]"

    def __repr__(self):
        return self.__str__()

    def __contains__(self, item):
        return self.node and self.node.__contains__(item)

    def draw_graph(self, step: int):
        graph = nx.DiGraph()

        nodes = [self.node]

        while len(nodes) > 0:
            node = nodes.pop()

            if not node:
                continue

            graph.add_node(node.id, label=f"{node.value} \nh: {node.height}\nb: {node.balance}")

            if node.left:
                nodes.append(node.left)
                graph.add_edge(node.id, node.left.id)

            if node.right:
                nodes.append(node.right)
                graph.add_edge(node.id, node.right.id)

        viz = nx.nx_agraph.to_agraph(graph)
        viz.layout(prog='dot')

        viz.draw(f"./graph-{step}.svg", 'svg')

        pass


def validate_is_avl(root_node: Node) -> bool:
    queue = [root_node]

    while len(queue) > 0:
        node = queue.pop()

        right_node = node.right
        left_node = node.left
        balance = node.__balance__()

        assert balance in [0, 1, -1], f"Node {node} is not balanced: {balance}"

        if right_node:
            assert node.value <= right_node.value, f"Node {node} value is greater than its right node"

            min_right = right_node.min_value()

            assert node < min_right, f"Node {node} value is greater than right value: {min_right}"

            queue.append(right_node)

        if left_node:
            assert node.value >= left_node.value, f"Node {node} value is lesser than its left node"

            max_left = left_node.max_value()

            assert node > max_left, f"Node {node} value is lesser than left value: {max_left}"

            queue.append(left_node)

    return True


def main():
    avl = AVLTree()

    # values = [1,8,2,5,9,3,6,7]
    values = [1, 2, 3, 4, 5, 6, 7, 8]

    for i, value in enumerate(values):
        avl.insert(value)
        avl.draw_graph(i)

    print(avl)

    avl.draw_graph(1234)


if __name__ == '__main__':
    main()
