import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node1", TextType.ITALIC, "urrrl")
        node4 = TextNode("This is a text node1", TextType.ITALIC, )
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node4, node3)

if __name__ == "__main__":
    unittest.main()