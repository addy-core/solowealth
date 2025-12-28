# SoloWealth - Desktop Application Build Guide



## 🚀 How to Build

**Run this single command:**
```bash
python build_desktop.py
```

This will:
1. Build the Python backend as `SoloWealth-Backend.exe`
2. Package it with Electron into a portable folder

## 📦 What Gets Created

```
electron-dist/
└── SoloWealth-win32-x64/    ← The App Folder
    ├── SoloWealth.exe       ← Run this!
    └── ... (resources)
```

## 📝 How to Distribute

1. Right-click the `SoloWealth-win32-x64` folder
2. Select **Send to -> Compressed (zipped) folder**
3. Send the `.zip` file to anyone!

They just unzip it and double-click `SoloWealth.exe`.

## 🔧 Requirements for Building

- Python 3.x
- Node.js
- (Dependencies will be auto-installed)

