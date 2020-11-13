from astroidtools.infer_functions import register_transformations

register_transformations()

# from astroid import parse

# a = parse("os().open.start('hello')")
# print(a.body[0].value.repr_tree())
