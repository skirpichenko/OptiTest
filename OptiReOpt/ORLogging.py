import logging
import json
import numpy as np
import threading 

log_lock = threading.Lock()

OR_BASE_LOGGER = 'optireopt'

class NumpyEncoder(json.JSONEncoder):
    MAX_ELEMENTS = 10
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            if obj.ndim != 1:
                return f"ndarray shape {obj.shape}"
            else:
                return str(obj)
        return super().default(obj)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        # ['args', 'created', 'exc_info', 'exc_text', 'filename', 'funcName', 
        # 'getMessage', 'levelname', 'levelno', 'lineno', 'module', 'msecs', 
        # 'msg', 'name', 'pathname', 'process', 'processName', 'relativeCreated', 
        # 'stack_info', 'thread', 'threadName']
        log_record = {
            'dt': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'name': record.name,
#            'thread': threading.get_ident(),
            'message': record.getMessage(),
            'data': record.args, 
        }
        return json.dumps(log_record, cls=NumpyEncoder)


class CustomFileHandler(logging.Handler):
    def __init__(self, filename, mode='a', encoding=None, delay=False):
        # Initialize the parent class
        super().__init__()
        self.baseFilename = filename
        self.mode = mode
        self.encoding = encoding
        # Open the file in the specified mode
        # self.file = open(filename, mode, encoding=encoding)

    def emit(self, record):
        try:
            # Format the log message
            log_message = self.format(record)

            # Write the log message to the file
            # self.file.write(log_message + '\n')
            # self.file.flush()  # Ensure the message is written immediately

            # for yet unknown reason, the above lines loose some log messages
            # quick fix: open and close the file for each log message
            with log_lock, open(self.baseFilename, self.mode, encoding=self.encoding) as f:
                f.write(log_message + '\n')

        except Exception:
            self.handleError(record)

    def close(self):
        # Close the file
        # self.file.close()
        super().close()


class ORLogger(logging.Logger):
    def __init__(self, 
            name: str, 
            fname: str,
            level = logging.INFO
        ):
        super().__init__(f'{OR_BASE_LOGGER}.{name}') # optireopt.sublogger
        self.setLevel(level)
        self.name = name
        self.propagate = False
        self._handler = CustomFileHandler(fname) # logging.FileHandler(fname)
        self._handler.setFormatter(JsonFormatter())
        self.addHandler(self._handler)
        self.filename = fname

    def __del__(self):
        if self._handler is not None:
            self.removeHandler(self._handler)
            self._handler.close()
        # super().__del__()

    def into(self, *args, **kwargs):
        with log_lock:
            self.info(*args, **kwargs)
            self._handler.flush()


def get_logger(name: str, fname: str) -> ORLogger:
    base_logger = getattr(get_logger, '_logger', None)
    if base_logger is None:
        logger = logging.getLogger(OR_BASE_LOGGER)
        logger.setLevel(logging.INFO)
        # add handlers, formatters, etc.
        setattr(get_logger, '_logger', logger)

    logger = ORLogger(name, fname)
    return logger