# 🚀 IKM AI Launcher

A lightweight Windows GUI for launching **[OpenWebUI](https://github.com/open-webui/open-webui)** and **[FastFlowLM (FLM)](https://github.com/FastFlowLM/FastFlowLM)** in separate PowerShell consoles.

> ⚠️ **Note:** This project does **not** bundle OpenWebUI, FLM, models, or any third-party binaries.  
> Users must install and configure them separately.

---

## 🔗 Quick Links
- 🔥 [**FastFlowLM (FLM)**](https://github.com/FastFlowLM/FastFlowLM)
- 🌐 [**OpenWebUI**](https://github.com/open-webui/open-webui)
- 📦 [**Download Latest Release**](../../releases/latest)

---

## 🖥️ Requirements
- Windows 10/11  
- Installed and configured [OpenWebUI](https://github.com/open-webui/open-webui)  
- Installed [FastFlowLM (FLM)](https://github.com/FastFlowLM/FastFlowLM)

---

## 📥 Download
Grab the latest `.exe` from the [**Releases**](../../releases/latest) section.

---

## ⚙️ Usage
1. Download and run `IKM AI Launcher.exe`.
2. Enter:
   - **OpenWebUI Directory**
   - **Host/Port**
   - **CORS** (defaults to `http://localhost:*`)
3. Click **Launch Both Servers** to start OpenWebUI and FLM.
4. Click **Stop All Servers** to stop both.

---

## 🔒 Security Notes
- Intended for **localhost use only**.
- No telemetry or data collection.

---

## 🛠️ Build from Source
```powershell
pip install pyinstaller
pyinstaller .\IKM_AI_Launcher.py --onefile --windowed --name "IKM AI Launcher" --icon .\IKM.ico --add-data ".\IKM.ico;."
