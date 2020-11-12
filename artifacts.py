class Artifact():
    def __init__(self, path=None, project_name=None, status=None, version=None, io=None):
        self.path = path
        self.project_name = project_name
        self.status = status
        self.version = version
        self.io = io
        if self.path is None:
            raise ValueError(f'The path for Object {self.__class__.__name__} should not be empty')


class Dataset(Artifact):
    def __init__(self, dsets=None, steps=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dsets = dsets
        self.steps = steps


class Model(Artifact):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Config(Artifact):
    # TODO: Add some code that can handle different configuration files (json, yaml, ini, etc...)
    def __init__(self, dset=None, step=None, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Code(Artifact):
    def __init__(self, steps=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.steps = steps


class Params(Artifact):
    # TODO: Add some code that can handle different configuration files (json, yaml, ini, etc...) to extract params
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
