from pathlib import Path
from watcher import setup_logger, start_watcher, run_forever

logger = setup_logger(log_file=Path("watcher.log"))

path = Path(
    r"C:\Users\DELL\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm"
    r"\LocalState\sessions\B7AF7A014325C70D65D45E4162CE8581436F7572"
    r"\transfers\2026-06"
)

observer = start_watcher(path, recursive=False, logger=logger)
run_forever(observer, logger)
