# SoloWealth Desktop App Builder
# build.py - Creates standalone .exe using PyInstaller

import subprocess
import sys
import os

def build_exe():
    """Build the SoloWealth desktop application"""
    print("=" * 50)
    print("SoloWealth Desktop App Builder")
    print("=" * 50)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build command
    print("\n🔨 Building executable...")
    
    build_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "SoloWealth",
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
        "--console",  # Keep console for debugging, use --windowed for no console
        "main.py"
    ]
    
    try:
        subprocess.check_call(build_cmd)
        print("\n" + "=" * 50)
        print("✅ BUILD SUCCESSFUL!")
        print("=" * 50)
        print(f"\n📁 Executable location: {os.path.join(os.getcwd(), 'dist', 'SoloWealth.exe')}")
        print("\n📌 To run the app:")
        print("   1. Navigate to the 'dist' folder")
        print("   2. Double-click 'SoloWealth.exe'")
        print("   3. Open browser to http://127.0.0.1:8000")
        print("\n💡 The finance.db will be created in the same folder as the .exe")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
