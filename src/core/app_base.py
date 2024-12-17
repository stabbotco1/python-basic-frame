from src.core.initialize_project import initialize_project
initialize_project()

from src.core.logger import SingletonLogger
logger = SingletonLogger.get_logger()

# Main program execution
def main():
    logger.info("Main started")

    # Load menu from JSON file


if __name__ == "__main__":
    main()
