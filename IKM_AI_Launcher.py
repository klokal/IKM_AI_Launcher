#By Ilias Kalliakmanis
#V1 - 07/09/2025

import os
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import shutil
import sys

if sys.platform.startswith("win"):
    try:
        import ctypes
        PROCESS_PER_MONITOR_DPI_AWARE = 2
        ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def resource_path(rel_path: str) -> str:

    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel_path)


def _kill_tree(pid: int) -> bool:
    res = subprocess.run(
        ["taskkill", "/PID", str(pid), "/T", "/F"],
        capture_output=True,
        text=True
    )
    return res.returncode == 0 or "SUCCESS" in (res.stdout + res.stderr).upper()

class ServerLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IKM AI Launcher")
        self.processes = {}
        self.is_running = False


        self._init_style()


        BG = "#0097A7"
        root.configure(bg=BG)


        try:
            root.tk.call('tk', 'scaling', 1.5)
        except Exception:
            pass


        outer = ttk.Frame(root, padding=20, style="Card.TFrame")
        outer.grid(sticky="nsew")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        title = ttk.Label(outer, text="IKM AI Launcher", style="Title.TLabel")
        title.grid(row=0, column=0, columnspan=2, pady=(0, 16), sticky="w")


        default_openwebui_dir = r"%LOCALAPPDATA%\OpenWebUI"
        default_cors = "*"
        default_host = "127.0.0.1"
        default_port = "8080"


        config = ttk.LabelFrame(outer, text="Configuration", padding=16, style="Card.TLabelframe")
        config.grid(row=1, column=0, columnspan=2, sticky="nsew")
        for i in range(2):
            config.columnconfigure(i, weight=1)

        ttk.Label(config, text="OpenWebUI Directory:", style="Body.TLabel")\
            .grid(row=0, column=0, sticky="e", padx=(0,12), pady=8)
        self.var_dir = tk.StringVar(value=default_openwebui_dir)
        ttk.Entry(config, textvariable=self.var_dir, width=48, style="Filled.TEntry")\
            .grid(row=0, column=1, sticky="we", pady=8)

        ttk.Label(config, text="CORS Origin:", style="Body.TLabel")\
            .grid(row=1, column=0, sticky="e", padx=(0,12), pady=8)
        self.var_cors = tk.StringVar(value=default_cors)
        ttk.Entry(config, textvariable=self.var_cors, width=48, style="Filled.TEntry")\
            .grid(row=1, column=1, sticky="we", pady=8)

        ttk.Label(config, text="Host:", style="Body.TLabel")\
            .grid(row=2, column=0, sticky="e", padx=(0,12), pady=8)
        self.var_host = tk.StringVar(value=default_host)
        ttk.Entry(config, textvariable=self.var_host, width=48, style="Filled.TEntry")\
            .grid(row=2, column=1, sticky="we", pady=8)

        ttk.Label(config, text="Port:", style="Body.TLabel")\
            .grid(row=3, column=0, sticky="e", padx=(0,12), pady=8)
        self.var_port = tk.StringVar(value=default_port)
        ttk.Entry(config, textvariable=self.var_port, width=12, style="Filled.TEntry")\
            .grid(row=3, column=1, sticky="w", pady=8)


        btns = ttk.Frame(outer, padding=(0, 14, 0, 0), style="Card.TFrame")
        btns.grid(row=2, column=0, columnspan=2, sticky="we")
        ttk.Button(btns, text="Launch Both Servers", command=self.launch_both, style="Blue.TButton")\
            .grid(row=0, column=0, padx=(0,12))
        ttk.Button(btns, text="Stop All Servers", command=self.stop_processes, style="Blue.TButton")\
            .grid(row=0, column=1)


        self.status = tk.StringVar(value="")
        ttk.Label(outer, textvariable=self.status, style="Caption.TLabel")\
            .grid(row=3, column=0, columnspan=2, sticky="w", pady=(14,0))

        for i in range(2):
            outer.columnconfigure(i, weight=1)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


    def _init_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        CYAN_BG = "#0097A7"
        CARD_BG = "#B2EBF2"
        BLUE = "#1976D2"
        BLUE_HOVER = "#1565C0"
        BLUE_DARK = "#0D47A1"
        TEXT = "#0f172a"

        style.configure(".", font=("Segoe UI", 12))
        style.configure("Title.TLabel", font=("Segoe UI Semibold", 18), background=CYAN_BG, foreground="white")
        style.configure("Body.TLabel",  font=("Segoe UI", 12), background=CARD_BG, foreground=TEXT)
        style.configure("Caption.TLabel", font=("Segoe UI", 11), background=CYAN_BG, foreground="white")

        style.configure("TFrame", background=CYAN_BG)
        style.configure("Card.TFrame", background=CYAN_BG)
        style.configure("Card.TLabelframe", background=CARD_BG, foreground=BLUE_DARK, relief="groove")
        style.configure("Card.TLabelframe.Label", background=CARD_BG, foreground=BLUE_DARK, font=("Segoe UI Semibold", 13))

        style.configure("Filled.TEntry",
                        fieldbackground="white",
                        background="white",
                        foreground=TEXT,
                        bordercolor=BLUE_DARK)

        style.configure("Blue.TButton",
                        background=BLUE,
                        foreground="white",
                        padding=(16, 8),
                        borderwidth=0)
        style.map("Blue.TButton",
                  background=[("active", BLUE_HOVER), ("pressed", BLUE_DARK)],
                  foreground=[("disabled", "#cbd5e1")])


    def set_status(self, msg):
        self.status.set(msg)
        self.root.update_idletasks()

    def _expand_env(self, path_text):
        txt = path_text.strip()
        if txt.upper().startswith("LOCALAPPDATA\\"):
            return os.path.join(os.environ.get("LOCALAPPDATA", ""), txt.split("\\", 1)[1])
        return os.path.expandvars(txt)

    def _find_openwebui_exe(self):
        exe = shutil.which("open-webui") or shutil.which("open-webui.exe")
        if exe:
            return exe
        appdata = os.environ.get("APPDATA", "")
        return os.path.join(appdata, "Python", "Python312", "Scripts", "open-webui.exe")


    def start_open_webui(self, host, port, openwebui_dir, cors_origin):
        openwebui_exe = self._find_openwebui_exe()
        ps_cmd = (
            f'$env:OPEN_WEBUI_DIR="{openwebui_dir}"; '
            f'$env:CORS_ALLOW_ORIGIN="{cors_origin}"; '
            f'& "{openwebui_exe}" serve --host {host} --port {port}'
        )
        proc = subprocess.Popen(
            ["powershell", "-NoExit", "-Command", ps_cmd],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        return proc.pid, proc

    def start_flm(self, host, port):

        ps_cmd = f'flm serve deepseek-r1-0528:8b --host {host} --port {port}'
        proc = subprocess.Popen(
            ["powershell", "-NoExit", "-Command", ps_cmd],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        return proc.pid, proc

    def _thread_launch_both(self):
        try:
            self.is_running = True
            self.set_status("Starting OpenWebUI...")
            host = self.var_host.get().strip() or "127.0.0.1"
            port = int(self.var_port.get().strip())

            openwebui_dir = self._expand_env(self.var_dir.get())
            cors_origin = self.var_cors.get().strip() or "*"

            pid1, proc1 = self.start_open_webui(host, port, openwebui_dir, cors_origin)
            self.processes[pid1] = proc1
            time.sleep(1.5)

            self.set_status("Starting FLM...")
            pid2, proc2 = self.start_flm(host, port + 1)
            self.processes[pid2] = proc2

            self.set_status(f"Started {len(self.processes)} services (OpenWebUI:{port}, FLM:{port+1}).")
        except Exception as e:
            self.set_status(f"Error: {e}")
        finally:
            self.is_running = False

    def launch_both(self):
        if self.is_running:
            return
        t = threading.Thread(target=self._thread_launch_both, daemon=True)
        t.start()

    def stop_processes(self):
        stopped = 0
        for pid, proc in list(self.processes.items()):
            try:
                if _kill_tree(pid):
                    stopped += 1
            except Exception:
                pass
            finally:
                self.processes.pop(pid, None)
        self.set_status(f"Stopped {stopped} services.")

    def on_close(self):
        if self.processes:
            if messagebox.askyesno("Quit", "Stop all launched servers before exiting?"):
                self.stop_processes()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()

    try:
        root.iconbitmap(resource_path("IKM.ico"))
    except Exception:
        pass

    app = ServerLauncherApp(root)


    root.update_idletasks()
    w, h = 780, 540
    x = (root.winfo_screenwidth()  - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.minsize(700, 500)

    root.mainloop()
