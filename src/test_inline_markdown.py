import unittest
from textnode import TextNode, TextType
from inline_markdown import (split_nodes_delimiter, extract_markdown_links, 
                             extract_markdown_images, split_nodes_image, 
                             split_nodes_link, text_to_textnodes)

class TestSplitNodesDelimiter(unittest.TestCase):
        def test_one_textnode(self):
            node = TextNode("This is text with a `code block` word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

            v_node0 = TextNode("This is text with a ", TextType.TEXT)
            v_node1 = TextNode("code block", TextType.CODE)
            v_node2 = TextNode(" word", TextType.TEXT)

            self.assertEqual(new_nodes[0], v_node0)
            self.assertEqual(new_nodes[1], v_node1)
            self.assertEqual(new_nodes[2], v_node2)
        
            node0 = TextNode("This is text with a `code block` word", TextType.TEXT)
            node1 = TextNode("This is `code block` wor", TextType.TEXT)
            node2 = TextNode("T `code block` w", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node0,node1,node2], "`", TextType.CODE)            
        
            v_node0 = TextNode("This is text with a ", TextType.TEXT)
            v_node1 = TextNode("code block", TextType.CODE)
            v_node2 = TextNode(" word", TextType.TEXT)

        def test_multiple_textnode(self):
            node0 = TextNode("This is text with a `code block` word", TextType.TEXT)
            node1 = TextNode("This is `code block` wor", TextType.TEXT)
            node2 = TextNode("T `code block` w", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node0,node1,node2], "`", TextType.CODE)            
        
            v_node0 = TextNode("This is text with a ", TextType.TEXT)
            v_node1 = TextNode("code block", TextType.CODE)
            v_node2 = TextNode(" word", TextType.TEXT)
            
            v_node3 = TextNode("This is ", TextType.TEXT)
            v_node4 = TextNode("code block", TextType.CODE)
            v_node5 = TextNode(" wor", TextType.TEXT)
            
            v_node6 = TextNode("T ", TextType.TEXT)
            v_node7 = TextNode("code block", TextType.CODE)
            v_node8 = TextNode(" w", TextType.TEXT)
            #=========================================================
            self.assertEqual(new_nodes[0], v_node0)
            self.assertEqual(new_nodes[1], v_node1)
            self.assertEqual(new_nodes[2], v_node2)
            
            self.assertEqual(new_nodes[3], v_node3)
            self.assertEqual(new_nodes[4], v_node4)
            self.assertEqual(new_nodes[5], v_node5)
            
            self.assertEqual(new_nodes[6], v_node6)
            self.assertEqual(new_nodes[7], v_node7)
            self.assertEqual(new_nodes[8], v_node8)


        def test_different_types_of_nodes(self):
            node = TextNode("This is text with a **code block** word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

            v_node0 = TextNode("This is text with a ", TextType.TEXT)
            v_node1 = TextNode("code block", TextType.BOLD)
            v_node2 = TextNode(" word", TextType.TEXT)

            self.assertEqual(new_nodes[0], v_node0)
            self.assertEqual(new_nodes[1], v_node1)
            self.assertEqual(new_nodes[2], v_node2)

            node = TextNode("This is text with a _code block_ word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

            v_node0 = TextNode("This is text with a ", TextType.TEXT)
            v_node1 = TextNode("code block", TextType.ITALIC)
            v_node2 = TextNode(" word", TextType.TEXT)

            self.assertEqual(new_nodes[0], v_node0)
            self.assertEqual(new_nodes[1], v_node1)
            self.assertEqual(new_nodes[2], v_node2)


        def test_delim_bold_double(self):
            node = TextNode(
                "This is text with a **bolded** word and **another**", TextType.TEXT
            )
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
            self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("bolded", TextType.BOLD),
                    TextNode(" word and ", TextType.TEXT),
                    TextNode("another", TextType.BOLD),
                ],
                new_nodes,
            )
        
        def test_extract_markdown_images(self):
            matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            )
            self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
        def test_extract_markdown_links(self):
            matches = extract_markdown_links(
                "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
            )
            self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TestExtracLinkImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
class TestInlineMarkdownToNodes(unittest.TestCase):
    def test_convert(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            node
        )
    
    def test_convert_no_bold(self):
        text = "This is text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            node
        )

if __name__ == "__main__":
    unittest.main()