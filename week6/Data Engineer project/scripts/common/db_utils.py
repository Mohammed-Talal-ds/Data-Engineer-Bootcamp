from sqlalchemy import create_engine
import yaml

def load_config(config_path='config/settings.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_engine(db_type, config):
    """Returns a SQLAlchemy engine based on the config file."""
    if db_type == 'sqlite':
        return create_engine(f"sqlite:///{config['sqlite_path']}")
    
    db_cfg = config.get(db_type)
    return create_engine(
        f"postgresql://{db_cfg['user']}:{db_cfg['password']}@{db_cfg['host']}:{db_cfg['port']}/{db_cfg['database']}"
    )