
import os
import subprocess
import sys

def run():
    # Get base path (handles temp dir extraction for --onefile)
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Path to the bundled Electron exe
    # We bundle the folder as 'app_root'
    # App name changed to AddyWealth.exe
    exe_path = os.path.join(base_path, "app_root", "AddyWealth.exe")
    
    # Run it
    if os.path.exists(exe_path):
        subprocess.call([exe_path] + sys.argv[1:])
    else:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, f"Could not find app at: {exe_path}", "Error", 16)

if __name__ == "__main__":
    # Hide console window
    run()
