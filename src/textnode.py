from enum import Enum

class TextType(Enum):
    TEXT = ""
    BOLD = "****"
    ITALIC = "__"
    CODE_TEXT = "``"
    LINK = "[]()"
    IMG = "![]()"

class TextNode:
    def __init__(self, txt, txt_type, url=None):
        self.text = txt
        self.text_type = txt_type
        self.url = url

    def __eq__(self, value):
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
