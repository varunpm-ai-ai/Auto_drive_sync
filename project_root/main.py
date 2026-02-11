from pathlib import Path
import signal
import sys
import time
from core.watcher import start_watcher
from core.pipeline import run_pipeline
from core.organizer import resolve_destination
from core.uploader import upload_file
from core.watcher import setup_logger


# Configuration

WATCH_PATH = Path(
    r"C:\Users\DELL\AppData\Local\Packages"
    r"\5319275A.WhatsAppDesktop_cv1g1gvanyjgm"
    r"\LocalState\sessions"
    r"\9E758E5FBD9E42BA75D4383657E3F345E0986DCD"
    r"\transfers"
    r""
)

SOURCE = "whatsapp"


# Main file handling logic

def handle_file(path: Path, logger):
    logger.info(f"Processing file: {path}")

    try:
        result = run_pipeline(path, source=SOURCE)

        dest = resolve_destination(
            result.metadata,
            result.classification,
            result.decision,
        )

        file_id = upload_file(
            local_path=path,
            logical_drive_path=dest,
        )

        logger.info(f"Uploaded to Drive: {dest} (file_id={file_id})")

    except Exception as e:
        logger.exception(f"Failed to process file {path}: {e}")


# Main Function
def main():
    logger = setup_logger()

    logger.info("Starting Auto Drive Sync...")

    observer = start_watcher(
        WATCH_PATH,
        recursive=True,
        logger=logger,
        on_file_detected=lambda p: handle_file(Path(p), logger),
    )

    def shutdown(signum, frame):
        logger.info("Shutdown signal received. Stopping watcher...")
        observer.stop()
        observer.join()
        logger.info("Watcher stopped. Exiting.")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown(None, None)


if __name__ == "__main__":
    main()
