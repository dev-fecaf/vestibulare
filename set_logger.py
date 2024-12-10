from loguru import logger


logger.add(
    'events.log',
    level='DEBUG',
    rotation='100 MB',
    retention='365 days',
    compression='zip'
)
