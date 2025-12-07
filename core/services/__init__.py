import logging

# Get a logger instance for the 'app' logger, as defined in settings.py.
# This is the recommended logger for all application-level logging.
logger = logging.getLogger('app')

# --- EXAMPLES OF HOW TO USE THE LOGGER ---

# logger.debug("This is a debug message. It's useful for detailed debugging.")
# logger.info("This is an info message. Use it for general operational entries.")
# logger.warning("This is a warning message. Use it to indicate something unexpected happened.")
# logger.error("This is an error message. Use it when something has gone wrong.")
# logger.critical("This is a critical message. Use it for very serious errors.")

# You can also include extra context in your logs, which is very useful for JSON logging.
# extra_context = {
#     'user_id': 'some_user_id',
#     'request_id': 'some_request_id',
# }
# logger.info("User performed an action.", extra=extra_context)
