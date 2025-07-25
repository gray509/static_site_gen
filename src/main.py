from textnode import TextNode, TextType
from markdown_to_node import *
import os, shutil
import sys

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_content_to_directory("./static", "./docs")
    
    content = os.path.abspath("./content")
    template = os.path.abspath("template.html")
    destination = os.path.abspath("./docs")
    
    generate_pages_recursive(content, template, destination, basepath)

def copy_content_to_directory(source, destination, boolean= False):
    source = os.path.abspath(source)
    destination = os.path.abspath(destination)
    if not boolean:
        if os.path.exists(destination):
            shutil.rmtree(destination)
        os.makedirs(destination)
        boolean = True
    
    if not os.path.exists(destination) and not os.path.isfile(source) :
        os.mkdir(destination)
        
    if os.path.isfile(source):
        shutil.copy(source, destination)
        return 
    
    for item in os.listdir(source):
        i_source = os.path.join(source, item)
        i_destination = os.path.join(destination, item)
        copy_content_to_directory(i_source, i_destination, boolean)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_path = os.path.abspath(from_path)
    template_path = os.path.abspath(template_path)
    dest_path = os.path.abspath(dest_path)
    
    with open(from_path, "r") as file:
        content = file.read()
    
    html_node = markdown_to_html_node(content) 
    html = html_node.to_html()
    title = extract_title(content)

    with open(template_path, "r") as file:
        template_content = file.read()
    
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html)
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')

    if not os.path.exists(dest_path):
        dirs = os.path.dirname(dest_path)
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    with open(dest_path, "w") as file:
        file.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.isfile(dir_path_content) and dir_path_content.endswith(".md"):
        dest_dir_path = dest_dir_path.replace("md", "html")
        generate_page(dir_path_content, template_path, dest_dir_path, basepath)
        return
    
    if not os.path.exists(dest_dir_path) and not os.path.isfile(dir_path_content) :
        os.mkdir(dest_dir_path)

    if os.path.isdir(dir_path_content):
        for item in os.listdir(dir_path_content):
            i_content = os.path.join(dir_path_content, item)
            i_dest = os.path.join(dest_dir_path, item)
            generate_pages_recursive(i_content, template_path, i_dest, basepath)
        
main()