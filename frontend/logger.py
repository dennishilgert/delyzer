import logging

def setup_logger():
    """
    Sets up a logger named "frontend" that logs both to the console (stream) and a file ('frontend.log'). The logger is set at the INFO level.
    
    Args:
        None.
    
    Returns:
        logger (logging.Logger): A Logger object to be used for logging messages.
        
    Tests:
        *Ensure that the function returns a Logger object
        *Ensure that the file handler is added to the logger
    """

    logger = logging.getLogger("frontend")
    logger.setLevel(logging.INFO)
    
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler('frontend.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
