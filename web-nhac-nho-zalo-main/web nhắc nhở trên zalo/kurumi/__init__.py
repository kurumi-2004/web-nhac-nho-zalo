from .bot import KurumiBot
from .config import Config
from .database import Database
from .utils import Utils
from .logger import Logger

__version__ = "1.0.0"
__author__ = "Trae AI"
__license__ = "MIT"

# Initialize core components
config = Config()
db = Database()
utils = Utils()
logger = Logger()

# Create bot instance
bot = KurumiBot(config=config, db=db, utils=utils, logger=logger)

# Export main components
__all__ = [
    'KurumiBot',
    'Config', 
    'Database',
    'Utils',
    'Logger',
    'bot',
    'config',
    'db',
    'utils',
    'logger'
]
