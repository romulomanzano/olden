import logging
import config
import uuid

FORMATTER = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")


def logged(class_):
    logger = logging.getLogger(class_.__name__)
    formatter = FORMATTER
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    class_.logger = logger
    return class_


def get_generic_logger(name):
    """
    Get logger for functions
    :param name: name of calling file
    :return: object
    """
    # Set logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = FORMATTER
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def unique_id():
    return str(uuid.uuid4().hex)
