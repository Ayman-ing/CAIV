"""
Logging configuration
"""
import logging
import sys
from typing import Dict, Any

def setup_logging(level: str = "INFO", format_type: str = "standard") -> None:
    """Setup application logging"""
    
    # Define log formats
    formats = {
        "standard": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        "json": '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
    }
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=formats.get(format_type, formats["standard"]),
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Suppress some verbose loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)