"""Logger for parser-Service."""
# STDLIB
import logging
from pathlib import Path

LOG_FILENAME = 'log.txt'

log_directory = Path('././logs')
log_directory.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=Path(log_directory, LOG_FILENAME),
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(name='logger')
