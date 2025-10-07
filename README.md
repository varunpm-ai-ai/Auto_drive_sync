# Auto Sort Notes

# Auto Sort Notes 📝✨

**Auto Sort Notes** is a Python-based automation tool designed to help students and professionals **organize and upload notes** effortlessly. It connects with your cloud storage (Google Drive, Google classroom, etc.) and automatically sorts, renames, and uploads your files according to predefined rules.

---

## Features 🚀

- **Automatic Sorting:** Organize notes by subject, date, or custom tags.  
- **Cloud Integration:** Supports Google Drive and Google classroom, (OAuth authentication).  
- **Cross-Platform:** Works on PC and mobile (via PyDroid).  
- **Minimal Setup:** Simple configuration and ready-to-use scripts.  
- **Resume-Ready Project:** Demonstrates real-world Python automation and cloud integration.

---

## Installation 💻

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/auto-sort-not
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the script:
```bash
python main.py
```

### 4. After successful login, you’ll see:
The authentication flow has completed. You may close this window.

### 5. The script will now have access to your cloud storage and automatically start sorting and uploading notes.

## Configuration 
Folder paths: Update config.py (or similar) with your local note directories.
Sorting rules: Define custom rules in rules.py (e.g., by subject, file type, or date).
Cloud provider: By default, Google Drive is supported. You can extend it to other providers.

## Mobile Usage 
Use PyDroid to run the script on Android.
Ensure the correct Android storage paths are set (/storage/emulated/0/...).
Keep the app open during uploads; background execution may not be stable.

## Contributing
Contributions are welcome! If you want to:
Add new cloud providers like one Drive and more or 
Improve sorting rules
Optimize performance
…feel free to fork the repo, make changes, and submit a pull request.

## License
This project is open-source under the MIT License. See LICENSE for details.

## Acknowledgements
Python community for libraries like os, shutil, and google-api-python-client.
Inspiration from personal productivity workflows and automation tools.
