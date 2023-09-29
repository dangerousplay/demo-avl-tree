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


if __name__ == "__main__":
    unittest.main()
