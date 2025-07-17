from enum import Enum
import re
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        if block == "":
            continue
        clean_blocks.append(block.strip())

    return clean_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    
    if block.startswith("```") and block.startswith("```"):
        return BlockType.CODE
    
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if block[0] == ">":
        m = block.split("\n")
        for l in m:
            if l[0] != ">":
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
        
    if block[:2] == "- ":
        m = block.split("\n")
        for l in m:
            if l[:2] != "- ":
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    if block[:3] == "1. ":
        m = block.split("\n")
        i = 1
        for l in m:
            if l[:3] == f"{i}. ":
                i += 1

        if i - 1 == len(m):
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH



        
            
