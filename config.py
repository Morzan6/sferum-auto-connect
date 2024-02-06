import logging
import sys

SESSION_DATA = ''

stdout_handler = logging.StreamHandler(stream=sys.stdout)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[stdout_handler],
)

LOGGER = logging.getLogger(__name__)
