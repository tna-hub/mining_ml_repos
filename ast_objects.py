import ast


class Imports(ast.NodeVisitor):
    def visit_Import(self, node):
        for imp in node.names:
            return imp.name, imp.asname

    def visit_ImportFrom(self, node):
        print("In ImportFrom")
        for imp in node.names:
            return node.module, imp.name, imp.asname, node.level

