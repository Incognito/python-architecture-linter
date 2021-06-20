import astroid

from python_architecture_linter.lint_provider_class import provider_class_linter
from python_architecture_linter.read_file import File, ProjectFileScanner


class FileParser:
    def to_ast(self, file: File):
        string_file = file.get_contents()
        return astroid.parse(string_file, path=file.get_path().absolute())


def validate_provider(file: File):
    ast_provider_file = FileParser().to_ast(file)

    # todo duplicate validation from logic allowed in method
    allow_list = (
        astroid.nodes.Import,
        astroid.nodes.ImportFrom,
        astroid.nodes.ClassDef,
    )
    for node in ast_provider_file.body:
        if not isinstance(node, allow_list):
            # todo need a clean to emit and collect violations
            print("violation")

    # todo check if there are import rules too

    provider_classes = filter(lambda node: isinstance(node, astroid.nodes.ClassDef), node)
    for provider_class in provider_classes:
        print(provider_class_linter(provider_classes))


def lint(path):
    files = ProjectFileScanner().get_files_in_project(path)

    # rule: modules with providers should be on the root level of a module
    # rule: provider must not be in files other than provider.py
    # rule: instances only created in provider (except for DTOs)
    # rule: runtime modules have a run.py

    provider_files = filter(lambda file: file.get_path().name == "provider.py", files)
    for provider_file in provider_files:
        # rule: provider may be in module/provider.py
        results = validate_provider(provider_file)
        print(results)


path = "/home/brian/python-architecture-linter/python_architecture_linter/tests/cases/modular_provider_architecture"  # noqa: E501
lint(path)

deny_list = (
    astroid.nodes.Arguments,
    astroid.nodes.Assert,
    astroid.nodes.AsyncFor,
    astroid.nodes.AsyncFunctionDef,
    astroid.nodes.AsyncWith,
    astroid.nodes.Attribute,
    astroid.nodes.AugAssign,
    astroid.nodes.Await,
    astroid.nodes.BinOp,
    astroid.nodes.BoolOp,
    astroid.nodes.Break,
    astroid.nodes.Compare,
    astroid.nodes.Comprehension,
    astroid.nodes.Continue,
    astroid.nodes.Decorators,
    astroid.nodes.DelAttr,
    astroid.nodes.Delete,
    astroid.nodes.DelName,
    astroid.nodes.DictComp,
    astroid.nodes.DictUnpack,
    astroid.nodes.ExceptHandler,
    astroid.nodes.Exec,
    astroid.nodes.Expr,
    astroid.nodes.For,
    astroid.nodes.FormattedValue,
    astroid.nodes.FunctionDef,
    astroid.nodes.GeneratorExp,
    astroid.nodes.Global,
    astroid.nodes.If,
    astroid.nodes.IfExp,
    astroid.nodes.Import,
    astroid.nodes.ImportFrom,
    astroid.nodes.Index,
    astroid.nodes.JoinedStr,
    astroid.nodes.Keyword,
    astroid.nodes.Lambda,
    astroid.nodes.ListComp,
    astroid.nodes.Module,
    astroid.nodes.Nonlocal,
    astroid.nodes.Print,
    astroid.nodes.Raise,
    astroid.nodes.Repr,
    astroid.nodes.TryExcept,
    astroid.nodes.TryFinally,
    astroid.nodes.Unknown,
    astroid.nodes.While,
    astroid.nodes.With,
    astroid.nodes.Yield,
    astroid.nodes.YieldFrom,
)

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
