import astroid


def class_name_validator(class_node: astroid.nodes.ClassDef):
    if not class_node.name.endswith("Provider"):
        return "Provider class names must end with the word Provider"
