class Artifact():
    def __init__(self, path=None, project_name=None, status=None, version=None):
        self.path = path
        self.project_name = project_name
        self.status = status
        self.version = version
        if self.path is None:
            raise ValueError(f'The path for Object {self.__class__.__name__} should not be empty')


class Dataset(Artifact):
    def __init__(self, dset=None, step=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dset = dset
        self.step = step

class
