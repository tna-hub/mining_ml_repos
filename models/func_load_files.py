import pprint

from sqlalchemy import Integer, Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from models import Base

assoc_native_func_param = Table('assoc_native_func_arg', Base.metadata,
                                Column('native_func_id', Integer, ForeignKey('native_func.id')),
                                Column('param_id', Integer, ForeignKey('param.id'))
                                )

assoc_lib_func_param = Table('assoc_lib_func_arg', Base.metadata,
                             Column('lib_func_id', Integer, ForeignKey('lib_func.id')),
                             Column('param_id', Integer, ForeignKey('param.id'))
                             )
assoc_custom_func_param = Table('assoc_custom_func_arg', Base.metadata,
                                Column('custom_func_id', Integer, ForeignKey('custom_func.id')),
                                Column('param_id', Integer, ForeignKey('param.id'))
                                )


class NativeFunc(Base):
    __tablename__ = 'native_func'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Association rule
    params = relationship(
        "Param",
        secondary=assoc_native_func_param)


class Lib(Base):
    __tablename__ = 'lib'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lib_funcs = relationship('LibFunc', backref='lib', lazy='dynamic')


class LibFunc(Base):
    __tablename__ = 'lib_func'
    id = Column(Integer, primary_key=True)
    lib_id = Column(ForeignKey('lib.id'))
    name = Column(String)
    lib_name = Column(String)

    # Association rule
    params = relationship(
        "Param",
        secondary=assoc_lib_func_param)


class CustomFunc(Base):
    __tablename__ = 'custom_func'
    id = Column(Integer, primary_key=True)
    code_id = Column(Integer, ForeignKey('code.id'))
    repo_id = Column(Integer, ForeignKey('repo.id'))
    #native_func_called = Column(Integer, ForeignKey('native_func.id'))
    #lib_func_called = Column(Integer, ForeignKey('lib_func.id'))
    name = Column(String)
    def_in_file = Column(Integer, ForeignKey('element.id'))

    # Association rule
    params = relationship(
        "Param",
        secondary=assoc_custom_func_param)


class Param(Base):
    __tablename__ = 'param'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    position = Column(Integer)


s_funcs = {'PIL': {'open': {'fparam_name': 'fp',
                            'fparam_position': 1,
                            'mparam_name': 'mode',
                            'mparam_position': 2,
                            'mparam_types': 'String',
                            'mvalues': 'r:r',
                            'set_mode_from_name': 'r'}},
           'cv2': {'imread': {'fparam_name': 'path',
                              'fparam_position': 1,
                              'mparam_name': None,
                              'mparam_position': None,
                              'mparam_types': None,
                              'mvalues': None,
                              'set_mode_from_name': 'r'}},
           'h5py': {'File': {'fparam_name': 'name',
                             'fparam_position': 1,
                             'mparam_name': 'mode',
                             'mparam_position': 2,
                             'mparam_types': 'String',
                             'mvalues': 'r:r;r+:rw;w:w;a:w',
                             'set_mode_from_name': None}},
           'io': {'open': {'fparam_name': 'file',
                           'fparam_position': 1,
                           'mparam_name': 'mode',
                           'mparam_position': 2,
                           'mparam_types': 'String',
                           'mvalues': 'r:r;a:w;w:w;x:w',
                           'set_mode_from_name': None},
                  'open_code': {'fparam_name': 'path',
                                'fparam_position': 1,
                                'mparam_name': None,
                                'mparam_position': None,
                                'mparam_types': None,
                                'mvalues': None,
                                'set_mode_from_name': 'r'}},
           'json': {'load': {'fparam_name': 'fp',
                             'fparam_position': 1,
                             'mparam_name': None,
                             'mparam_position': None,
                             'mparam_types': None,
                             'mvalues': None,
                             'set_mode_from_name': 'r'}},
           'keras': {'save': {'fparam_name': 'filepath',
                              'fparam_position': 1,
                              'mparam_name': None,
                              'mparam_position': None,
                              'mparam_types': None,
                              'mvalues': None,
                              'set_mode_from_name': 'w'}},
           'native': {'open': {'fparam_name': 'file',
                               'fparam_position': 1,
                               'mparam_name': 'mode',
                               'mparam_position': 2,
                               'mparam_types': 'String',
                               'mvalues': 'r:r;a:w;w:w;x:w;r+:rw;w+:rw',
                               'set_mode_from_name': None}},
           'numpy': {'dump': {'fparam_name': 'file',
                              'fparam_position': 1,
                              'mparam_name': None,
                              'mparam_position': None,
                              'mparam_types': None,
                              'mvalues': None,
                              'set_mode_from_name': 'w'},
                     'load': {'fparam_name': 'file',
                              'fparam_position': 1,
                              'mparam_name': None,
                              'mparam_position': None,
                              'mparam_types': None,
                              'mvalues': None,
                              'set_mode_from_name': 'r'},
                     'loadtxt': {'fparam_name': 'fname',
                                 'fparam_position': 1,
                                 'mparam_name': None,
                                 'mparam_position': None,
                                 'mparam_types': None,
                                 'mvalues': None,
                                 'set_mode_from_name': 'r'},
                     'memmap': {'fparam_name': 'filename',
                                'fparam_position': 1,
                                'mparam_name': 'mode',
                                'mparam_position': 2,
                                'mparam_types': 'String',
                                'mvalues': 'r+:rw;r:r;w+:rw;c:w',
                                'set_mode_from_name': None},
                     'save': {'fparam_name': 'file',
                              'fparam_position': 1,
                              'mparam_name': None,
                              'mparam_position': None,
                              'mparam_types': None,
                              'mvalues': None,
                              'set_mode_from_name': 'w'},
                     'savetxt': {'fparam_name': 'fname',
                                 'fparam_position': 1,
                                 'mparam_name': None,
                                 'mparam_position': None,
                                 'mparam_types': None,
                                 'mvalues': None,
                                 'set_mode_from_name': 'w'},
                     'savez': {'fparam_name': 'file',
                               'fparam_position': 1,
                               'mparam_name': None,
                               'mparam_position': None,
                               'mparam_types': None,
                               'mvalues': None,
                               'set_mode_from_name': 'w'},
                     'savez_compressed': {'fparam_name': 'file',
                                          'fparam_position': 1,
                                          'mparam_name': None,
                                          'mparam_position': None,
                                          'mparam_types': None,
                                          'mvalues': None,
                                          'set_mode_from_name': 'w'},
                     'tofile': {'fparam_name': 'fid',
                                'fparam_position': 1,
                                'mparam_name': None,
                                'mparam_position': None,
                                'mparam_types': None,
                                'mvalues': None,
                                'set_mode_from_name': 'w'}},
           'os': {'open': {'fparam_name': 'file',
                           'fparam_position': 1,
                           'mparam_name': 'flags',
                           'mparam_position': 2,
                           'mparam_types': 'Object',
                           'mvalues': 'os.O_RDONLY:r;os.O_WRONLY:w;os.O_RDWR:rw;os.O_APPEND:w',
                           'set_mode_from_name': None}},
           'pandas': {'ExcelWriter': {'fparam_name': 'path',
                                      'fparam_position': 1,
                                      'mparam_name': 'mode',
                                      'mparam_position': 2,
                                      'mparam_types': 'String',
                                      'mvalues': 'w:w;a:w',
                                      'set_mode_from_name': 'w'},
                      'read_csv': {'fparam_name': 'filepath_or_buffer',
                                   'fparam_position': 1,
                                   'mparam_name': None,
                                   'mparam_position': None,
                                   'mparam_types': None,
                                   'mvalues': None,
                                   'set_mode_from_name': 'r'},
                      'read_excel': {'fparam_name': 'io',
                                     'fparam_position': 1,
                                     'mparam_name': None,
                                     'mparam_position': None,
                                     'mparam_types': None,
                                     'mvalues': None,
                                     'set_mode_from_name': 'r'},
                      'read_fwf': {'fparam_name': 'filepath_or_buffer',
                                   'fparam_position': 1,
                                   'mparam_name': None,
                                   'mparam_position': None,
                                   'mparam_types': None,
                                   'mvalues': None,
                                   'set_mode_from_name': 'r'},
                      'read_pickle': {'fparam_name': 'filepath_or_buffer',
                                      'fparam_position': 1,
                                      'mparam_name': None,
                                      'mparam_position': None,
                                      'mparam_types': None,
                                      'mvalues': None,
                                      'set_mode_from_name': 'r'},
                      'read_spss': {'fparam_name': 'filepath',
                                    'fparam_position': 1,
                                    'mparam_name': None,
                                    'mparam_position': None,
                                    'mparam_types': None,
                                    'mvalues': None,
                                    'set_mode_from_name': 'r'},
                      'read_table': {'fparam_name': 'filepath_or_buffer',
                                     'fparam_position': 1,
                                     'mparam_name': None,
                                     'mparam_position': None,
                                     'mparam_types': None,
                                     'mvalues': None,
                                     'set_mode_from_name': 'r'},
                      'to_csv': {'fparam_name': 'path_or_buf',
                                 'fparam_position': 1,
                                 'mparam_name': None,
                                 'mparam_position': None,
                                 'mparam_types': None,
                                 'mvalues': None,
                                 'set_mode_from_name': 'w'}},
           'skimage': {'imread': {'fparam_name': 'fname',
                                  'fparam_position': 1,
                                  'mparam_name': None,
                                  'mparam_position': None,
                                  'mparam_types': None,
                                  'mvalues': None,
                                  'set_mode_from_name': 'r'},
                       'imsave': {'fparam_name': 'fname',
                                  'fparam_position': 1,
                                  'mparam_name': None,
                                  'mparam_position': None,
                                  'mparam_types': None,
                                  'mvalues': None,
                                  'set_mode_from_name': 'w'}},
           'sklearn': {'load_files': {'fparam_name': 'container_path',
                                      'fparam_position': 1,
                                      'mparam_name': None,
                                      'mparam_position': None,
                                      'mparam_types': None,
                                      'mvalues': None,
                                      'set_mode_from_name': 'r'}},
           'tensorflow': {'get_file': {'fparam_name': 'fname',
                                       'fparam_position': 1,
                                       'mparam_name': None,
                                       'mparam_position': None,
                                       'mparam_types': None,
                                       'mvalues': None,
                                       'set_mode_from_name': 'r'},
                          'load_model': {'fparam_name': 'filepath',
                                         'fparam_position': 1,
                                         'mparam_name': None,
                                         'mparam_position': None,
                                         'mparam_types': None,
                                         'mvalues': None,
                                         'set_mode_from_name': 'r'},
                          'read_file': {'fparam_name': 'filename',
                                        'fparam_position': 1,
                                        'mparam_name': None,
                                        'mparam_position': None,
                                        'mparam_types': None,
                                        'mvalues': None,
                                        'set_mode_from_name': 'r'},
                          'save_model': {'fparam_name': 'filepath',
                                         'fparam_position': 2,
                                         'mparam_name': None,
                                         'mparam_position': None,
                                         'mparam_types': None,
                                         'mvalues': None,
                                         'set_mode_from_name': 'w'},
                          'write_file': {'fparam_name': 'filename',
                                         'fparam_position': 1,
                                         'mparam_name': None,
                                         'mparam_position': None,
                                         'mparam_types': None,
                                         'mvalues': None,
                                         'set_mode_from_name': 'w'}},
           'torch': {'load': {'fparam_name': 'f',
                              'fparam_position': 1,
                              'mparam_name': None,
                              'mparam_position': None,
                              'mparam_types': None,
                              'mvalues': None,
                              'set_mode_from_name': 'r'},
                     'save': {'fparam_name': 'f',
                              'fparam_position': 2,
                              'mparam_name': None,
                              'mparam_position': None,
                              'mparam_types': None,
                              'mvalues': None,
                              'set_mode_from_name': 'w'}},
           'utils': {'load_data': {'fparam_name': 'directory',
                                   'fparam_position': 1,
                                   'mparam_name': None,
                                   'mparam_position': None,
                                   'mparam_types': None,
                                   'mvalues': None,
                                   'set_mode_from_name': 'r'}}}
