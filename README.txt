# IKM AI Launcher

A small Windows GUI that launches **OpenWebUI** and **FLM** in separate PowerShell consoles.
**This project does not bundle OpenWebUI, FLM, models, or any third-party binaries.**

## Requirements
- Windows 10/11
- OpenWebUI and FLM installed separately

## Download
Grab the latest `.exe` from **Releases**.

## Usage
1. Run the EXE.
2. Set OpenWebUI directory, host/port, and CORS (defaults to `http://localhost:*`).
3. Click **Launch Both Servers**. Click **Stop All Servers** to stop.

## Security Notes
- Intended for localhost.
- No telemetry or data collection.

## Build from Source
```powershell
pip install pyinstaller
pyinstaller .\IKM_AI_LaunchER.py --onefile --windowed --name "IKM AI Launcher" --icon .\IKM.ico --add-data ".\IKM.ico;."
