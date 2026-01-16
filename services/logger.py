import os
import logging
from logging.handlers import RotatingFileHandler

def configure_logging(app, logfile="logs/app.log", level=logging.INFO):
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    handler = RotatingFileHandler(logfile, maxBytes=1048576, backupCount=3)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    handler.setLevel(level)
    app.logger.addHandler(handler)
    app.logger.setLevel(level)
    wlog = logging.getLogger("werkzeug")
    wlog.addHandler(handler)
    wlog.setLevel(level)
    return app.logger
