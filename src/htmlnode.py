class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return None
        s = []
        for att in self.props:
            s.append(f'{att}="{self.props[att]}"')
        
        return " ".join(s)
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, propss=None):
        super().__init__(tag, value, props=propss)
    
    def to_html(self):
        if not self.value:
            raise ValueError("No value found in this Leaf node")
        if not self.tag:
            return self.value
        
        if self.props:
            s = f'<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>'
        else:
            s =f"<{self.tag}>{self.value}</{self.tag}>"

        return s
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, propss=None):
        super().__init__(tag, children=children, props=propss)

    def to_html(self):
        if not self.tag:
            raise ValueError("No value tag in this Parent node")
        
        if self.children == None or len(self.children) == 0 :
            raise ValueError("Parent node missing Parent or Leaf node childrens")
        
        for child in self.children:
            if not isinstance(child, LeafNode) and not isinstance(child, ParentNode):
                raise ValueError("Child object is not the correct object, has to ParentNode or Leafnode")

            if isinstance(child, LeafNode):
                if not child.value:
                    raise ValueError("No value found for the children")
        
        s = ""
        if self.props:
            s = f'<{self.tag} {self.props_to_html()}>'
        else:
            s = f'<{self.tag}>'

        for child in self.children:
            s += child.to_html()
        
        s+= f"</{self.tag}>"

        return s
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    