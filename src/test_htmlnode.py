import unittest
from htmlnode import LeafNode, ParentNode, HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            'class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
    
    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node0 = LeafNode("a", 
                         "Click here!",
                          {"href":"https://boot.dev",
                           "target": "_blank"})
        self.assertEqual(node0.to_html(), '<a href="https://boot.dev" target="_blank">Click here!</a>') 


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],)
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("b", [])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(
            str(context.exception),
            "Parent node missing Parent or Leaf node childrens"
        )
        parent_node1 = ParentNode("b", None)
        with self.assertRaises(ValueError) as context:
            parent_node1.to_html()
        self.assertEqual(
            str(context.exception),
            "Parent node missing Parent or Leaf node childrens"
        )
    
    def test_to_html_incorrrect_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("b", [child_node,1])
        
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(
            str(context.exception),
            "Child object is not the correct object, has to ParentNode or Leafnode"
        )

        parent_node1 = ParentNode("b", [1])
        with self.assertRaises(ValueError) as context:
            parent_node1.to_html()
        self.assertEqual(
            str(context.exception),
            "Child object is not the correct object, has to ParentNode or Leafnode"
        )

    

        
if __name__ == "__main__":
    unittest.main()