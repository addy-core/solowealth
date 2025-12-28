
import os
import subprocess
import sys
import shutil

def build_single_file_wrapper():
    """Create a single .exe wrapper using PyInstaller"""
    print("\n" + "=" * 60)
    print("Step 5: Creating Single File Executable (Wrapper Only)")
    print("=" * 60)
    
    # Find source dir dynamically
    dist_dir = "electron-dist"
    # Look for AddyWealth folder
    found_dirs = [d for d in os.listdir(dist_dir) if os.path.isdir(os.path.join(dist_dir, d)) and "AddyWealth" in d and not d.endswith(".zip")]
    
    if not found_dirs:
        print("❌ Source folder not found!")
        return False
        
    source_dir_name = found_dirs[0]
    source_folder = os.path.join(dist_dir, source_dir_name)
    print(f"📂 Source: {source_folder}")

    # Create the launcher script
    launcher_code = f"""
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
        ctypes.windll.user32.MessageBoxW(0, f"Could not find app at: {{exe_path}}", "Error", 16)

if __name__ == "__main__":
    # Hide console window
    run()
"""
    
    with open("launcher.py", "w") as f:
        f.write(launcher_code)
        
    print("🔨 Packaging entire app into one EXE (this may take a minute)...")
    
    # Build the wrapper
    # We add the ENTIRE Electron app folder as data
    build_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--icon", "electron/icon.ico",
        "--name", "AddyWealth-App",
        f"--add-data", f"{source_folder};app_root",
        "--clean",
        "launcher.py"
    ]
    
    try:
        subprocess.check_call(build_cmd)
        print("✅ Single file created successfully!")
        
        # Cleanup
        if os.path.exists("launcher.py"):
            os.remove("launcher.py")
        if os.path.exists("launcher.spec"):
             # Keep spec for debug if needed, but usually delete
             try: os.remove("launcher.spec") 
             except: pass
            
        print("\nChecking dist folder...")
        if os.path.exists(os.path.join("dist", "AddyWealth-App.exe")):
            print("✅ CONFIRMED: dist/AddyWealth-App.exe exists!")
        else:
            print("❌ ERROR: File missing from dist!")

        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Wrapper build failed: {e}")
        return False

if __name__ == "__main__":
    build_single_file_wrapper()
