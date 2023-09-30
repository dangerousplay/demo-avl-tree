import unittest
from avl import AVLTree, validate_is_avl, Node


class AVLTestCase(unittest.TestCase):
    def test_large_right_rotation(self):
        total_nodes = 0

        avl = AVLTree()

        for i in range(10, 0, -1):
            avl.insert(i)
            total_nodes += 1

        avl.draw_graph('test-right')

        self.assertTrue(validate_is_avl(avl.node))
        self.assertEqual(total_nodes, avl.__len__())

    def test_large_left_rotation(self):
        total_nodes = 0

        avl = AVLTree()
        for i in range(1, 11):
            avl.insert(i)
            total_nodes += 1

        avl.draw_graph('test-left')

        self.assertTrue(validate_is_avl(avl.node))
        self.assertEqual(total_nodes, avl.__len__())

    def test_left_right_rotation(self):
        total_nodes = 5
        root_node_value = 5

        # this is the tree represented:
        #   x
        #    \
        #   (x+5)
        #    /
        #  (x+1)
        #    \
        #    (x+2)
        right_node = Node(value=root_node_value+5,
                          left=Node(value=root_node_value+1,
                                    right=Node(value=root_node_value+2)
                                    )
                          )

        root_node = Node(value=root_node_value, right=right_node)

        avl = AVLTree()
        avl.node = root_node

        avl.insert(root_node_value + 4)

        avl.draw_graph('test-left-right')

        self.assertTrue(validate_is_avl(avl.node))
        self.assertEqual(total_nodes, avl.__len__())

    def test_right_left_rotation(self):
        total_nodes = 5
        root_node_value = 5

        # this is the tree represented:
        #      x
        #     /
        #   (x-5)
        #     \
        #    (x-1)
        #    /
        #  (x-3)
        left_node = Node(value=root_node_value-5,
                         right=Node(value=root_node_value-1,
                                    left=Node(value=root_node_value-3)
                                    )
                         )

        root_node = Node(value=root_node_value, left=left_node)

        avl = AVLTree()
        avl.node = root_node

        avl.insert(root_node_value - 4)

        avl.draw_graph('test-right-left')

        self.assertTrue(validate_is_avl(avl.node))
        self.assertEqual(total_nodes, avl.__len__())

    def test_contains_exists(self):
        avl = AVLTree()

        items = 10

        for i in range(items):
            avl.insert(i)

        for i in range(items):
            self.assertTrue(i in avl, f"{i} should exists in the tree")

    def test_contains_not_exists(self):
        avl = AVLTree()

        items = 10

        for i in range(items):
            avl.insert(i)

        for i in range(items):
            self.assertFalse(i + items in avl, f"{i + items} should not exists in the tree")
            self.assertFalse(i - items in avl, f"{i - items} should not exists in the tree")

    def test_validate_avl_right_value(self):
        root_node = Node(value=15, left=Node(value=5), right=Node(value=6))

        with self.assertRaises(Exception):
            validate_is_avl(root_node)

    def test_validate_avl_left_value(self):
        root_node = Node(value=4, left=Node(value=5), right=Node(value=6))

        with self.assertRaises(Exception):
            validate_is_avl(root_node)

    def test_validate_avl_left_balanced(self):
        left_node = Node(value=5)

        for value in range(5):
            left_node = left_node.insert(value)

        root_node = Node(value=4, left=left_node, right=Node(value=6))

        with self.assertRaises(Exception):
            validate_is_avl(root_node)

    def test_validate_avl_right_balanced(self):
        right_node = Node(value=5)

        for value in range(5):
            right_node = right_node.insert(value)

        root_node = Node(value=4, left=Node(value=6), right=right_node)

        with self.assertRaises(Exception):
            validate_is_avl(root_node)

    def test_delete_leaf(self):
        avl = AVLTree()
        amount = 10
        expect_nodes = []

        for value in range(amount):
            avl.insert(value)
            expect_nodes.append(value)

        for i in range(amount):
            if i % 2 == 0:
                remove_value = avl.node.min_value().value
            else:
                remove_value = avl.node.max_value().value

            avl.delete(remove_value)

            validate_is_avl(avl.node)

            expect_nodes.remove(remove_value)

            for value in expect_nodes:
                self.assertTrue(avl.__contains__(value), f"Should contain value {value}")

            self.assertFalse(avl.__contains__(remove_value), f"Should not contain value {remove_value}")

    def test_delete_root(self):
        avl = AVLTree()

        expect_nodes = []
        amount = 10

        for value in range(amount):
            expect_nodes.append(value)
            avl.insert(value)

        for i in range(amount):
            remove_value = avl.node.value

            avl.draw_graph(f"delete-root-{i}")

            avl.delete(remove_value)

            avl.draw_graph(f"delete-after-{i}")

            validate_is_avl(avl.node)

            expect_nodes.remove(remove_value)

            for node in expect_nodes:
                self.assertTrue(avl.__contains__(node), f"Should contain value {node}")

            self.assertFalse(avl.__contains__(remove_value), f"Should not contain value {remove_value}")

    def test_has_child(self):
        cases = [
            Node(value=2, left=Node(value=1), right=Node(value=3)),
            Node(value=2, left=Node(value=1)),
            Node(value=2, right=Node(value=3))
        ]

        for case in cases:
            self.assertTrue(case.has_child())

    def test_has_child_empty(self):
        node = Node(value=2)

        self.assertFalse(node.has_child())


if __name__ == "__main__":
    unittest.main()
