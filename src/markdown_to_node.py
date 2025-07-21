from block_markdown import *
from inline_markdown import *
from textnode import *
from htmlnode import *
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block = " ".join(block.split("\n"))
                parent_html_node = ParentNode("p",text_to_children(block))
            case BlockType.HEADING:
                i = 0
                while block[i] == "#":
                    i += 1
                parent_html_node = ParentNode(f"h{i}",text_to_children(block[i+1:]))
            case BlockType.QUOTE:
                lines = block.split("\n")
                new_lines = []
                for line in lines:
                    if not line.startswith(">"):
                        raise ValueError("invalid quote block")
                    new_lines.append(line.lstrip(">").strip())
                content = " ".join(new_lines)
                parent_html_node = ParentNode("blockquote",text_to_children(content))
            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                nodes = []
                for line in lines:
                    childrens = text_to_children(line[3:])
                    nodes.append(ParentNode("li", childrens))
                parent_html_node = ParentNode("ol",nodes)
            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                nodes = []
                for line in lines:
                    childrens = text_to_children(line[2:])
                    nodes.append(ParentNode("li", childrens))
                parent_html_node = ParentNode("ul",nodes)
            case BlockType.CODE:
                node = TextNode(block[4:-3], TextType.CODE)
                parent_html_node = ParentNode("pre",[text_node_to_html_node(node)])
        
        child_nodes.append(parent_html_node)
    return ParentNode("div", child_nodes)

def text_to_children(text):
    nodes = text_to_textnodes(text)
    leaf_nodes = []
    for node in nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    
    return leaf_nodes

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
         if block.startswith("# "):
             return block[2:]
    
    raise ValueError("No h1 header")