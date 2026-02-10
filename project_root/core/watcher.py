from __future__ import annotations
import os
import glob
import shutil
import sys
import logging
import time
from typing import Optional, Callable
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler,FileSystemEventHandler,FileSystemEvent


# logging 

def setup_logger(
    name: str = "media_watcher",
    level: int = logging.INFO,
    log_dir: Path = Path("logs"),
    log_file: str = "app.log",
    console: bool = True,
) -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # avoid duplicate handlers
    if logger.handlers:
        return logger

    # Ensure log exists
    log_dir.mkdir(exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # File handler 
    file_handler = logging.FileHandler(log_dir / log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler 
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# Event handler

class MediaEventHandler(FileSystemEventHandler):
    
    def __init__(self, logger: logging.Logger,on_file_detected: Optional[Callable[[str], None]] = None,):
        self.logger = logger
        self.on_file_detected = on_file_detected
        
    def _handle_file(self, path: str):
        if self.on_file_detected:
            self.on_file_detected(path)

    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        self.logger.info(f"File created: {event.src_path}")
        self._handle_file(event.src_path)

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        self.logger.info(f"File modified: {event.src_path}")
        self._handle_file(event.src_path)

    def on_moved(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        self.logger.info(
            f"File moved: {event.src_path} → {event.dest_path}"
        )
        self._handle_file(event.dest_path)

    def on_deleted(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        self.logger.warning(f"File deleted: {event.src_path}")
        self.logger.warning(f"File deleted: {event.src_path}")



def start_watcher(
    watch_path: Path,
    recursive: bool = False,
    logger: Optional[logging.Logger] = None,
    on_file_detected: Optional[Callable[[str], None]] = None,
) -> Observer: # type: ignore
    
    if not watch_path.exists():
        raise FileNotFoundError(f"Path does not exist: {watch_path}")
    
    if not watch_path.is_dir():
        raise IsADirectoryError(f"Not a directory: {watch_path}")
    
    logger = logger or setup_logger()
    
    logger.info(f"Starting watcher on: {watch_path}")
    
    event_handler = MediaEventHandler(
        logger,
        on_file_detected=on_file_detected,
        )
    observer = Observer()
    observer.schedule(
        event_handler,
        path=str(watch_path),  
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