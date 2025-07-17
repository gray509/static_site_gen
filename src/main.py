from textnode import TextNode, TextType
from markdown_to_node import *
def main():
    md = """
- This is **bolded** paragraph
- text in a p
- tag here

This is another paragraph with _italic_ text and `code` here

"""
    
    print(markdown_to_html_node(md).to_html())


main()