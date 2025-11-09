import logging
from notebackup.logger import setup_logger

def test_setup_logger():
    """
    Test that the logger is configured correctly.
    """
    logger = setup_logger()

    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.INFO
    assert not logger.propagate
    assert len(logger.handlers) == 1
    
    handler = logger.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    
    formatter = handler.formatter
    assert formatter._fmt == '%(asctime)s - %(levelname)s - %(message)s'
