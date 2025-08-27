import os
import sys
import logging


_PYTHON_EXEC = "C:/ILLOGIC_APP/Prism/2.0.16/app/Python311/Prism.exe"
_DEBUGPY_PATH = 'R:/devmaxime/virtualvens/sanitycheck/Lib/site-packages'
_LOG_FILE = 'R:/logs/debug/debug.log'


DEBUG_MODE = True
try:
    sys.path.append(_DEBUGPY_PATH)
    import debugpy
except:
    DEBUG_MODE = False


def create_logger(log_file):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger(__name__)
    
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    fileHandler = logging.FileHandler(log_file)
    fileHandler.setLevel(logging.DEBUG) 
    fileHandler.setFormatter(formatter)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.INFO)
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(formatter)
    
    logger.setLevel(logging.DEBUG)


def debug(port=5678, log_file=_LOG_FILE):
    logger: logging.Logger = create_logger(log_file)
    if not DEBUG_MODE:
        return
    
    debugpy.configure(python=_PYTHON_EXEC)
    try:
        debugpy.listen(port)
    except Exception as e:
        logger.info(e)
        return
    
    logger.info("Waiting for debugger attach")
    debugpy.wait_for_client()
