from __future__ import annotations
import os
import glob
import shutil
import sys
import logging
import time
from typing import Optional
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler,FileSystemEventHandler,FileSystemEvent


# logging 

def setup_logger(
    name: str = "media_watcher",
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
) -> logging.Logger:
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # avoiding duplicates
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    
    handler = (
        logging.FileHandler(log_file)
        if log_file
        else logging.StreamHandler()
    )
    
    # Formater
    handler.setFormatter(formatter)
    
    # Handler
    logger.addHandler(handler)
    
    return logger


# Event handler

class MediaEventHandler(FileSystemEventHandler):
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        self.logger.info(f"File created: {event.src_path}")

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        self.logger.info(f"File modified: {event.src_path}")

    def on_moved(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        self.logger.info(
            f"File moved: {event.src_path} → {event.dest_path}"
        )

    def on_deleted(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        self.logger.warning(f"File deleted: {event.src_path}")



def start_watcher(
    watch_path: Path,
    recursive: bool = False,
    logger: Optional[logging.Logger] = None,
) -> Observer: # type: ignore
    
    if not watch_path.exists():
        raise FileNotFoundError(f"Path does not exist: {watch_path}")
    
    if not watch_path.is_dir():
        raise IsADirectoryError(f"Not a directory: {watch_path}")
    
    logger = logger or setup_logger()
    
    logger.info(f"Starting watcher on: {watch_path}")
    
    event_handler = MediaEventHandler(logger)
    observer = Observer()
    observer.schedule(
        event_handler,
        path=str(watch_path),  # boundary conversion
        recursive=recursive,
    )
    observer.start()

    return observer


# Running until interupted 

def run_forever(observer: Observer, logger: logging.Logger) -> None: # type: ignore
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutdown requested. Stopping observer...")
        observer.stop()
    observer.join()
    logger.info("Observer stopped cleanly.")