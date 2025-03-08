from loguru import logger


logger.add(
    'logs/events.log',
    level='DEBUG',
    rotation='100 MB',
    retention='300 days',
    compression='zip'
)
