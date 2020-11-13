from astroid import nodes


class ASTObject:
    def __init__(self, name=None, filename=None, lineno=None, project_name=None, astroid_node=None):
        """

        :param name: The name of the object
        :param filename:
        :param lineno:
        :param project_name:
        :param astroid_node:
        """

        self.name = name
        self.filename = filename
        self.lineno = lineno if astroid_node is None else astroid_node.lineno
        self.project_name = project_name
        self.astroid_node = astroid_node

        if self.astroid_node is None:
            raise ValueError(f'The astroid node for Object {self.__class__.__name__} should not be empty')


class CodeFile(ASTObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_open_node(self, names: dict = None, start_from=None):
        """
        Extract all the functions used to open a file

        :rtype: Iterator[:class:`DataLoadFunc`]
        :param NodeNG start_from: Astroid node where to find the functions
        :param dict names: List of functions used to open files
        """
        if names is None:
            names = {}
        if names.__class__.__name__ != "dict":
            raise TypeError("The parameter names must be a dictionary")
        if not names:
            raise ValueError("should provide at least one function name in the parameter names")
        start_from = self.astroid_node if start_from is None else start_from
        name = None
        full_name = None
        for node in start_from.nodes_of_class(nodes.Call):
            if hasattr(node.func, "attrname"):
                name = node.func.attrname
                full_name = node.func.expr.as_string() + '.' + name
            elif hasattr(node.func, "name"):
                name = node.func.name
                full_name = name
            if name is not None and name in names.keys():
                d = DataLoadFunc(name=name, astroid_node=node, full_name=full_name, io=names[name], filename=self.filename)
                yield d


class DataLoadFunc(ASTObject):
    def __init__(self, full_name=None, ags=None, io: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.io = io
        self.full_name = full_name
        self.args = ags if ags is not None else self.set_args()

    def get_keywords(self, index=0):
        keywords = []
        for i, keyword in enumerate(self.astroid_node.keywords):
            index += i
            arg = Arg(name=keyword.arg, astroid_node=keyword, position=index)
            arg.get_value()
            keywords.append(arg)
        return keywords

    def get_arguments(self, index=0):
        arguments = []
        for i, arg in enumerate(self.astroid_node.args):
            index = i
            arg = Arg(astroid_node=arg, position=index)
            arguments.append(arg)
        return arguments, index + 1

    def set_args(self):
        last = 0
        res = []
        if self.astroid_node.args is not None:
            if len(self.astroid_node.args) > 0:
                res, last = self.get_arguments()
        if self.astroid_node.keywords is not None:
            res += self.get_keywords(last)
        return res
    # TODO: Add function to retrieve the argument that is used to store (1) artifact name and (2) the mode


class Arg(ASTObject):
    def __init__(self, position: int = None, value=None, value_found: bool = None, *args, **kwargs):
        """
        Argument of functions.

        :param position:
        :param value:
        :param value_found:
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.position = position
        self.value_found = value_found
        self.value = value if value is not None else self.get_value()

    def get_value(self):
        try:
            v = next(self.astroid_node.value.infer()) if self.astroid_node.__class__.__name__ == "Keyword" else next(
                self.astroid_node.infer())
        except Exception as e:
            v = e
        if v.__class__.__name__ == "Const":
            self.value_found = True
            return v.value
        else:
            return v
