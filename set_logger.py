from loguru import logger


logger.remove()

logger.add(
    'logs/events.log',
    level='DEBUG',
    rotation='100 MB',
    retention='365 days',
    compression='zip'
)
