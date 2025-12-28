# SoloWealth Desktop App Builder with Electron
# build_desktop.py - Creates standalone desktop app with native UI

import subprocess
import sys
import os
import shutil

def build_python_backend():
    """Build the Python backend as an executable"""
    print("=" * 60)
    print("Step 1: Building Python Backend")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    print("\n🔨 Building Python backend executable...")
    
    build_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "SoloWealth-Backend",
        "--add-data", "index.html;.",
        "--hidden-import", "uvicorn.logging",
        "--hidden-import", "uvicorn.protocols.http",
        "--hidden-import", "uvicorn.protocols.http.auto",
        "--hidden-import", "uvicorn.protocols.http.h11_impl",
        "--hidden-import", "uvicorn.protocols.websockets",
        "--hidden-import", "uvicorn.protocols.websockets.auto",
        "--hidden-import", "uvicorn.lifespan",
        "--hidden-import", "uvicorn.lifespan.on",
        "--hidden-import", "uvicorn.lifespan.off",
        "--windowed",  # No console window
        "--clean",
        "main.py"
    ]
    
    try:
        subprocess.check_call(build_cmd)
        print("✅ Python backend built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend build failed: {e}")
        return False

def prepare_electron_resources():
    """Copy the backend executable to Electron resources"""
    print("\n" + "=" * 60)
    print("Step 2: Preparing Electron Resources")
    print("=" * 60)
    
    backend_exe = os.path.join("dist", "SoloWealth-Backend.exe")
    resources_dir = os.path.join("electron", "resources")
    
    # Create resources directory
    os.makedirs(resources_dir, exist_ok=True)
    
    # Copy backend exe to resources
    if os.path.exists(backend_exe):
        dest = os.path.join(resources_dir, "SoloWealth-Backend.exe")
        shutil.copy2(backend_exe, dest)
        print(f"✅ Copied backend to: {dest}")
        
        # Also copy index.html
        if os.path.exists("index.html"):
            shutil.copy2("index.html", resources_dir)
            print("✅ Copied index.html")
        
        return True
    else:
        print(f"❌ Backend executable not found: {backend_exe}")
        return False

def build_electron_app():
    """Build the Electron desktop application"""
    print("\n" + "=" * 60)
    print("Step 3: Building Electron Desktop App")
    print("=" * 60)
    
    # Check if node_modules exists
    if not os.path.exists("node_modules"):
        print("📦 Installing Node.js dependencies...")
        try:
            subprocess.check_call(["npm", "install"], shell=True)
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Make sure Node.js is installed.")
            return False
            
    # Set local cache to avoid permission errors
    env = os.environ.copy()
    env["ELECTRON_BUILDER_CACHE"] = os.path.join(os.getcwd(), "build", "cache")
    os.makedirs(env["ELECTRON_BUILDER_CACHE"], exist_ok=True)
    
    print("\n🔨 Building Electron application (Portable Folder)...")
    try:
        # Use npm script which now runs electron-packager
        subprocess.check_call(["npm", "run", "build:win"], shell=True, env=env)
        print("✅ Electron app built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Electron build failed: {e}")
        return False

def create_zip_archive():
    """Create a zip archive of the built application"""
    print("\n" + "=" * 60)
    print("Step 4: Zipping for Distribution")
    print("=" * 60)
    
    source_dir = os.path.join("electron-dist", "SoloWealth-win32-x64")
    zip_name = os.path.join("electron-dist", "SoloWealth-App")
    
    if os.path.exists(source_dir):
        print("📦 Creating Zip archive...")
        shutil.make_archive(zip_name, 'zip', source_dir)
        print(f"✅ Created: {zip_name}.zip")
        return True
    else:
        print(f"❌ Source directory not found: {source_dir}")
        return False

def build_single_file_wrapper():
    """Create a single .exe wrapper using PyInstaller"""
    print("\n" + "=" * 60)
    print("Step 5: Creating Single File Executable")
    print("=" * 60)
    
    # Define source folder
    source_folder = os.path.join("electron-dist", "SoloWealth-win32-x64")
    if not os.path.exists(source_folder):
        print("❌ Source folder not found!")
        return False

    # Create the launcher script
    launcher_code = """
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
    exe_path = os.path.join(base_path, "SoloWealth-win32-x64", "SoloWealth.exe")
    
    # Run it
    if os.path.exists(exe_path):
        subprocess.call([exe_path] + sys.argv[1:])
    else:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, f"Could not find app at: {exe_path}", "Error", 16)

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
        "--name", "SoloWealth-App",
        f"--add-data", f"{source_folder};SoloWealth-win32-x64",
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
            os.remove("launcher.spec")
            
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Wrapper build failed: {e}")
        return False

def main():
    print("\n" + "🚀" * 30)
    print("SoloWealth Desktop Application Builder")
    print("Building Native Desktop App with Electron + Python")
    print("🚀" * 30 + "\n")
    
    # Step 1: Build Python backend
    if not build_python_backend():
        print("\n❌ Build process aborted.")
        sys.exit(1)
    
    # Step 2: Prepare Electron resources
    if not prepare_electron_resources():
        print("\n❌ Build process aborted.")
        sys.exit(1)
    
    # Step 3: Build Electron app
    if not build_electron_app():
        print("\n❌ Build process aborted.")
        sys.exit(1)
        
    # Step 4: Zip it (backup)
    create_zip_archive()
    
    # Step 5: Wrapper (The Requested Single File)
    build_single_file_wrapper()
    
    # Success!
    print("\n" + "=" * 60)
    print("✅✅✅ BUILD SUCCESSFUL! ✅✅✅")
    print("=" * 60)
    
    print("\n🎁 SINGLE FILE FOR SHARING:")
    print(f"   {os.path.join(os.getcwd(), 'dist', 'SoloWealth-App.exe')}")
    print("   (Send this ONE file to anyone)")
    
    print(f"\n� Original Folder (Faster startup):")
    print(f"   {os.path.join(os.getcwd(), 'electron-dist', 'SoloWealth-win32-x64')}")

if __name__ == "__main__":
    main()
