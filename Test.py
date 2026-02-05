# from pathlib import Path

# # Whats app foulder path
# WhatsAppFoulderPath = Path(r"C:\Users\DELL\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\LocalState\sessions\B7AF7A014325C70D65D45E4162CE8581436F7572\transfers\2026-06")

# if WhatsAppFoulderPath.exists():
#     print("Foulder Exhisits")
    
#     for iter in WhatsAppFoulderPath.iterdir():
#         if iter.is_file():
#             print(f"File : {iter.name}")
#         elif iter.is_dir():
#             print(f"Directory : {iter.name}")

# else:
#     print("Folder does not exist.")
    

# print(list(Path(r"C:\Users\DELL\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\LocalState\sessions\B7AF7A014325C70D65D45E4162CE8581436F7572\transfers\2026-06").iterdir()))

import logging

logger = logging.getLogger(__name__)
print(logger)

loginfo = logging.INFO
print(loginfo)