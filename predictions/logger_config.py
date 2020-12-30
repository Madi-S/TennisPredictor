import logging


def get_logger(child: str = None):
    if child:
        if not isinstance(child, str):
            raise TypeError('Child name for a logger must be a string')
        logger = logging.getLogger(f'TennisPredictor.{child}')
        return logger

    logger = logging.getLogger('TennisPredictor')

    fmt = logging.Formatter(
        '%(name)s:%(levelname)s:%(funcName)s - %(message)s')

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(fmt)

    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)

    return logger