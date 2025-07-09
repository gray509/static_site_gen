class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        s = []
        for att in self.props:
            s.append(f'{att}="{self.props[att]}"')
        
        return " ".join(s)
    
    def __repr__(self):
        return f"TAG: {self.tag}\nVALUE: {self.value}\nCHILDREN: {self.children}\nPRPOPS: {self.props}"
    