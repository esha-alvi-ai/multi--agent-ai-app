import logging
import os
from datetime import datetime

# Create logs folder if it doesn't exist
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Create log file with timestamp
log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
log_filepath = os.path.join(LOGS_DIR, log_filename)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler()
    ]
)

# Get logger
logger = logging.getLogger("AgenticAI")

def log_info(message):
    logger.info(message)

def log_warning(message):
    logger.warning(message)

def log_error(message):
    logger.error(message)

def log_debug(message):
    logger.debug(message)
