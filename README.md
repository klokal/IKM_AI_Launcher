

<h1 align="center">IKM AI Launcher</h1>

<p align="center">
  <a href="https://github.com/klokal/IKM_AI_Launcher/releases/latest">

  </a>
  <img alt="OS" src="https://img.shields.io/badge/Windows-10%2F11-blue?logo=windows">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-informational">
</p>

<p align="center">
  <img alt="Tag" src="https://img.shields.io/badge/NPU-Launcher-8A2BE2?labelColor=333333">
</p>

<p align="center">
  A lightweight Windows GUI that launches 
  <a href="https://github.com/open-webui/open-webui"><b>OpenWebUI</b></a> 
  and 
  <a href="https://github.com/FastFlowLM/FastFlowLM"><b>FastFlowLM (FLM)</b></a> 
  in separate PowerShell consoles for daily inference completely on Ryzen AI NPU equipped laptops.
  <br />
  <i>This project does not bundle OpenWebUI, FLM, models, or any third-party binaries.</i>
</p>

---

## 🔗 Quick Links
- 🔥 <a href="https://github.com/FastFlowLM/FastFlowLM"><b>FastFlowLM (FLM)</b></a>
- 🌐 <a href="https://github.com/open-webui/open-webui"><b>OpenWebUI</b></a>
- 📦 <a href="https://github.com/klokal/IKM_AI_Launcher/releases/latest"><b>Download Latest Release</b></a>

---

## 🖥️ Requirements
- Windows 10/11, Ryzen AI cpu equipped with XDNA NPU.
- Installed and configured <a href="https://github.com/open-webui/open-webui">OpenWebUI</a>
- Installed <a href="https://github.com/FastFlowLM/FastFlowLM">FastFlowLM (FLM)</a>

---

## ⚙️ Usage
1. Download and run `IKM AI Launcher.exe` from **Releases**.
2. Enter:
   - **OpenWebUI Directory**
   - **Host/Port**
   - **CORS** (defaults to `http://localhost:*`)
3. Click **Launch Both Servers** to start OpenWebUI and FLM.
4. Click **Stop All Servers** to stop both.

---

## 🔒 Security Notes
- Intended for **localhost** use.
- No telemetry or data collection.

---

## 🛠️ Build from Source
```powershell
pip install pyinstaller
pyinstaller .\IKM_AI_Launcher.py --onefile --windowed --name "IKM AI Launcher" --icon .\IKM.ico --add-data ".\IKM.ico;."
