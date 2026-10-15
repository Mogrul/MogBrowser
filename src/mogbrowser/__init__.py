from .options import Options
from .logger import load_logger

options = Options()
load_logger(options.debug)

debug = options.debug
scopes = options.scopes
thumbnail_path = options.thumbnail_path

from .data import Data
data = Data()