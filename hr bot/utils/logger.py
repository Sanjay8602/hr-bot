import logging

def setup_logger():
    """
    Configure logging for the application.
    Returns:
        logger: Configured logger instance
    """
    logger = logging.getLogger("HRChatbot")
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger