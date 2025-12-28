const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;
const PORT = 8000;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        minWidth: 1100,
        minHeight: 700,
        title: 'Addy Wealth - Personal Finance Tracker',
        icon: path.join(__dirname, 'icon.ico'),
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true
        },
        autoHideMenuBar: true,
        backgroundColor: '#0f0f1a'
    });

    // Wait for Python server to start, then load
    setTimeout(() => {
        mainWindow.loadURL(`http://127.0.0.1:${PORT}`);
    }, 2000);

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

function startPythonServer() {
    // Determine the path to backend executable
    const isDev = !app.isPackaged;
    let backendPath;

    if (isDev) {
        // Development: Look for the executable in dist folder or run Python directly
        const exePath = path.join(__dirname, '..', 'electron', 'resources', 'SoloWealth-Backend.exe');
        if (require('fs').existsSync(exePath)) {
            backendPath = exePath;
            console.log('Using bundled backend executable (dev mode)');
        } else {
            // Fallback to Python for development
            console.log('Backend exe not found, trying Python...');
            const pythonCommands = ['python', 'python3', 'py'];
            const scriptPath = path.join(__dirname, '..', 'main.py');

            function tryPython(index) {
                if (index >= pythonCommands.length) {
                    dialog.showErrorBox(
                        'Backend Not Found',
                        'Please run "python build_desktop.py" first to build the backend.'
                    );
                    app.quit();
                    return;
                }

                const pythonPath = pythonCommands[index];
                console.log(`Trying ${pythonPath}...`);

                pythonProcess = spawn(pythonPath, [scriptPath], {
                    cwd: path.dirname(scriptPath),
                    stdio: ['ignore', 'pipe', 'pipe']
                });

                pythonProcess.stdout.on('data', (data) => {
                    console.log(`Backend: ${data}`);
                });

                pythonProcess.stderr.on('data', (data) => {
                    console.error(`Backend Error: ${data}`);
                });

                pythonProcess.on('error', (err) => {
                    console.log(`${pythonPath} not found, trying next...`);
                    tryPython(index + 1);
                });

                pythonProcess.on('exit', (code) => {
                    if (code !== null && code !== 0) {
                        console.log(`Backend exited with code ${code}`);
                    }
                });
            }

            tryPython(0);
            return;
        }
    } else {
        // Production: Search for backend in multiple locations
        const possiblePaths = [
            // Sibling to executable (Root level) - Priority 1
            path.join(path.dirname(process.execPath), 'SoloWealth-Backend.exe'),
            // Standard Electron resources path
            path.join(process.resourcesPath, 'resources', 'SoloWealth-Backend.exe'),
            // Sibling to executable (common in unpacked)
            path.join(path.dirname(process.execPath), 'resources', 'SoloWealth-Backend.exe'),
            // Root of resources
            path.join(process.resourcesPath, 'SoloWealth-Backend.exe'),
            // Up one level from resources (sometimes flat)
            path.join(process.resourcesPath, '..', 'resources', 'SoloWealth-Backend.exe')
        ];

        backendPath = possiblePaths.find(p => require('fs').existsSync(p));

        if (!backendPath) {
            // Debugging: Show where we looked AND what is in the folders
            let fileList = "Unable to read directory";
            try {
                const resourcesDir = path.join(path.dirname(process.execPath), 'resources');
                const files = require('fs').readdirSync(resourcesDir);
                fileList = `Contents of ${resourcesDir}:\n${files.join('\n')}`;
            } catch (e) {
                fileList = `Error reading dir: ${e.message}`;
            }

            const debugMsg = `Looked in:\n${possiblePaths.join('\n')}\n\n${fileList}`;
            dialog.showErrorBox('Backend Not Found - File Search', debugMsg);
            app.quit();
            return;
        }

        console.log('Found backend at:', backendPath);
    }

    // Launch the backend executable
    console.log(`Starting backend from: ${backendPath}`);

    if (!require('fs').existsSync(backendPath)) {
        dialog.showErrorBox(
            'Backend Not Found',
            `Backend executable not found at: ${backendPath}\n\nPlease reinstall the application.`
        );
        app.quit();
        return;
    }

    pythonProcess = spawn(backendPath, [], {
        cwd: path.dirname(backendPath),
        stdio: ['ignore', 'pipe', 'pipe']
    });

    pythonProcess.stdout.on('data', (data) => {
        console.log(`Backend: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Backend Error: ${data}`);
    });

    pythonProcess.on('error', (err) => {
        console.error('Failed to start backend:', err);
        dialog.showErrorBox(
            'Backend Error',
            `Failed to start the backend server: ${err.message}`
        );
        app.quit();
    });

    pythonProcess.on('exit', (code) => {
        if (code !== null && code !== 0) {
            console.log(`Backend exited with code ${code}`);
        }
    });
}

function stopPythonServer() {
    if (pythonProcess) {
        pythonProcess.kill();
        pythonProcess = null;
    }
}

app.whenReady().then(() => {
    startPythonServer();
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    stopPythonServer();
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('before-quit', () => {
    stopPythonServer();
});
