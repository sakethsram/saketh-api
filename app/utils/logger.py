import logging

# Create logger
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)  

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

debug_file_handler = logging.FileHandler("debug_info.log")
debug_file_handler.setLevel(logging.DEBUG)

error_file_handler = logging.FileHandler("error.log")
error_file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
debug_file_handler.setFormatter(formatter)
error_file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(debug_file_handler)
logger.addHandler(error_file_handler)