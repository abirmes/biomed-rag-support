import sys
from pathlib import Path
from loguru import logger
from app.config.settings import settings

# Créer le dossier logs s'il n'existe pas
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configuration du logger
logger.remove()  # Retirer le handler par défaut

# Handler pour la console
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL,
)

# Handler pour le fichier
logger.add(
    settings.LOG_FILE,
    rotation="500 MB",
    retention="10 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level=settings.LOG_LEVEL,
    backtrace=True,
    diagnose=True,
)

logger.add(
    "logs/errors.log",
    rotation="100 MB",
    retention="30 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR",
    backtrace=True,
    diagnose=True,
)


def get_logger(name: str):

    return logger.bind(name=name)