import os
import logging
from datetime import datetime

def _logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    today = datetime.now()
    path = os.path.dirname(os.path.abspath(__file__))
    fh = logging.FileHandler(path + "{}log{}{}-{}-{}.log".format(os.sep, os.sep, today.year, today.month, today.day), encoding='utf-8')
    fmt = "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] - %(message)s"
    formatter = logging.Formatter(fmt)
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger



