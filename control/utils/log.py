import logging
from django.conf import settings

def logger(name):
    level = {
        3: logging.ERROR,
        2: logging.WARNING,
        1: logging.INFO,
        0: logging.DEBUG
    }.get(settings.VERBOSITY, logging.DEBUG)

    log = logging.getLogger(name=name)
    log.setLevel(level=level)

    fh = logging.FileHandler(settings.LOGFILE)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)-7s %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)
    return log
