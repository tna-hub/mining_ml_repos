from models import Base, config, asts, gits, code, func_load_files

if __name__ == '__main__':
    print('-----Initialising  Database-------')
    engine = config.init_db()
    metadata = Base.metadata
    metadata.create_all(engine)
    print('------------Finished!!------------------')