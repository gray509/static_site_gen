from textnode import TextNode, TextType
def main():
    test = TextNode("this is some test",  TextType.LINK, "https://www.boot.dev/lessons/cdae7fca-a7dc-4706-b2c5-7a03d66db1c9")
    print(test)


main()