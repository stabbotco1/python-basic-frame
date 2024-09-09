from src.core.logger import SingletonLogger
# from src.core.core_utilities import CoreUtilities

def main():
    # Get the logger instance
    logger = SingletonLogger.get_logger()

    # Log some messages
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

if __name__ == "__main__":
    main()
