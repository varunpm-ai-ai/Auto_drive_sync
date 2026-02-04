## Scope (LLD v1)

- Implementation of a Windows-based folder watcher for WhatsApp media directories, with event-driven detection of file creation, modification, and deletion.

- Deterministic media classification using file metadata (extension, size, MIME type) without any ML or heuristic inference.

- Pluggable cloud sync interfaces enabling upload, retry, and failure handling, abstracted from provider-specific logic.
