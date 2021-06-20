import astroid


def method_name_validator(func_node: astroid.nodes.FunctionDef):
    if not func_node.name.startswith(("provide_", "_provide_", "_create_", "__init__")):
        return f"invalid method name {func_node.name}"


def method_arguments_validator(func_node: astroid.nodes.FunctionDef):
    if func_node.name.startswith(("provide_", "_provide_")):
        if not func_node.args.as_string() == "self":
            return f"invalid arguments in method name {func_node.name}({func_node.args.as_string()}), should only receive self"


def method_logic_validator(func_node: astroid.nodes.FunctionDef):
    allow_list = (
        astroid.nodes.AnnAssign,
        astroid.nodes.Assign,
        astroid.nodes.AssignAttr,
        astroid.nodes.AssignName,
        astroid.nodes.Call,
        astroid.nodes.Const,
        astroid.nodes.Dict,
        astroid.nodes.Ellipsis,
        astroid.nodes.EmptyNode,
        astroid.nodes.ExtSlice,
        astroid.nodes.List,
        astroid.nodes.Name,
        astroid.nodes.Pass,
        astroid.nodes.Return,
        astroid.nodes.Set,
        astroid.nodes.SetComp,
        astroid.nodes.Slice,
        astroid.nodes.Starred,
        astroid.nodes.Subscript,
        astroid.nodes.Tuple,
        astroid.nodes.UnaryOp,
    )

    for node in func_node.body:
        if not isinstance(node, allow_list):
            return f"Logic found in {func_node.name}, but is not permitted inside provider. found {node.as_string()}. Solve this by moving logic outside of provider."


def method_object_creation_count(func_node: astroid.nodes.FunctionDef):
    def recursive_walk(node):
        try:
            for subnode in node.get_children():
                yield subnode
                yield from recursive_walk(subnode)

        except (AttributeError, TypeError):
            yield node

    creational_call_count = 0
    for node in recursive_walk(func_node):
        if isinstance(node, astroid.nodes.Call):
            function_path = node.func.as_string()
            if not (function_path.startswith("self.") or function_path.endswith("Provider")):
                creational_call_count += 1

    if creational_call_count > 2:
        return f"Too many business objects are created in {func_node.name}. This would create tight-coupling of object creation, which the provider aims to avoid"
