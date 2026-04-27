"""
Logging configuration
"""
import logging
import sys
from typing import Dict, Any

def setup_logging(level: str = "INFO", format_type: str = "standard") -> None:
    """Setup application logging"""
    import os
    
    # Ensure logs directory exists
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, "app.log")
    
    # Define log formats
    formats = {
        "standard": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        "json": '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
    }
    
    log_format = formats.get(format_type, formats["standard"])
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file)
        ]
    )
    
    # Suppress some verbose loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)