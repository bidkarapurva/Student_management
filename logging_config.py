import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Logs will be saved in app.log at the root
        logging.StreamHandler()  # Logs will also appear in the console
    ]
)

logger = logging.getLogger(__name__)
