import tkinter as tk
import subprocess
import webbrowser
import threading
import ctypes
import sys
import os

# ─────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────

APPS = {
    "whatsapp":        "5319275A.51895FA4EA97F_cv1g1gvanyjgm!App",
    "camera":          "microsoft.windows.camera:",
    "calculator":      "calc",
    "notepad":         "notepad",
    "paint":           "mspaint",
    "photos":          "ms-photos:",
    "vs code":         r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe",
    "vscode":          r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe",
    "tableau":         r"C:\Program Files\Tableau\Tableau 2024.1\bin\tableau.exe",
    "power bi":        r"C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe",
    "powerbi":         r"C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe",
    "mysql":           r"C:\Program Files\MySQL\MySQL Workbench 8.0\MySQLWorkbench.exe",
    "mysql workbench": r"C:\Program Files\MySQL\MySQL Workbench 8.0\MySQLWorkbench.exe",
    "excel":           r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "word":            r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "powerpoint":      r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
    "chrome":          r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "vlc":             r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "spotify":         "spotify:",
    "discord":         r"%LOCALAPPDATA%\Discord\Update.exe",
    "zoom":            r"%APPDATA%\Zoom\bin\Zoom.exe",
    "teams":           "msteams:",
    "file explorer":   "explorer",
    "explorer":        "explorer",
    "task manager":    "taskmgr",
    "settings":        "ms-settings:",
}

SITES = {
    "chatgpt":       ("https://chat.openai.com",           "Default"),
    "gmail":         ("https://mail.google.com",           "Default"),
    "youtube":       ("https://www.youtube.com",           "Default"),
    "github":        ("https://github.com",                "Default"),
    "linkedin":      ("https://www.linkedin.com",          "Default"),
    "whatsapp web":  ("https://web.whatsapp.com",          "Default"),
    "google":        ("https://www.google.com",            "Default"),
    "notion":        ("https://www.notion.so",             "Default"),
    "figma":         ("https://www.figma.com",             "Default"),
    "stackoverflow": ("https://stackoverflow.com",         "Default"),
    "kaggle":        ("https://www.kaggle.com",            "Default"),
    "colab":         ("https://colab.research.google.com", "Default"),
    "replit":        ("https://replit.com",                "Default"),
}

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CHROME_PROFILES = {
    "profile name":  "Default",
    "profile name":  "Profile number",
    "profile name":  "Profile number",
    "profile name":  "Profile number",
    "profile name":  "Profile number",
    "profile name":  "Profile number",
    "profile name":  "Profile number",
    "default": "Default",
}

# ─────────────────────────────────────────────
#  COMMAND LOGIC
# ─────────────────────────────────────────────

def open_url_in_profile(url, profile="Default"):
    subprocess.Popen([CHROME_PATH, f"--profile-directory={profile}", url])

def open_url_default(url):
    webbrowser.open(url)

def launch_app(name):
    key = name.lower().strip()
    for app_key, cmd in APPS.items():
        if key == app_key or key in app_key or app_key in key:
            try:
                exp = os.path.expandvars(cmd)
                if "!" in cmd:
                    subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{exp}"])
                elif cmd.endswith(":"):
                    os.startfile(exp)
                elif exp.lower().endswith(".lnk"):
                    os.startfile(exp)
                else:
                    subprocess.Popen(exp, shell=True)
                return True
            except Exception as e:
                print(f"App error: {e}")
    return False

def open_site(name, profile=""):
    key = name.lower().strip()
    for site_key, (url, default_profile) in SITES.items():
        if key == site_key or key in site_key or site_key in key:
            try:
                open_url_in_profile(url, profile if profile else default_profile)
            except Exception:
                open_url_default(url)
            return True
    return False

def smart_url(text):
    """
    Convert any user input into a proper https:// URL.
      'netflix'              → https://www.netflix.com
      'netflix.com'          → https://www.netflix.com
      'primevideo.com'       → https://www.primevideo.com
      'google.co.in'         → https://www.google.co.in
      'github.com/user'      → https://github.com/user
      'https://example.com'  → https://example.com  (unchanged)
      'google docs'          → https://www.googledocs.com  (spaces stripped)
    """
    t = text.strip()

    # already a full URL
    if t.startswith("http://") or t.startswith("https://"):
        return t

    # has a dot → treat as domain/path, just add https://
    if "." in t:
        base = t if t.startswith("www.") else t
        return f"https://{base}"

    # plain word(s) → strip spaces, wrap as .com
    domain = t.replace(" ", "").lower()
    return f"https://www.{domain}.com"


def handle_command(raw):
    cmd = raw.strip().lower()

    
    if cmd.startswith("open "):
        rest = raw.strip()[5:].strip()
        words = rest.split()

        # ── PRIORITY 1: last word is a known Chrome profile? ──────────
        if len(words) >= 2:
            profile_key = words[-1].lower()
            chrome_dir  = CHROME_PROFILES.get(profile_key)
            if chrome_dir:
                site_name = " ".join(words[:-1])

                # already a known site
                if open_site(site_name.lower(), chrome_dir):
                    return f"Opened {site_name}  [{words[-1].capitalize()}]"

                # smart URL conversion
                url = smart_url(site_name)
                open_url_in_profile(url, chrome_dir)
                return f"Opened {url}  [{words[-1].capitalize()}]"

        # ── PRIORITY 2: try launching a local app ─────────────────────
        if launch_app(rest):
            return f"Opened: {rest}"

        # ── PRIORITY 3: try a known site (default profile) ────────────
        if open_site(rest.lower()):
            return f"Opened: {rest}"

        # ── PRIORITY 4: smart URL fallback ────────────────────────────
        url = smart_url(rest)
        open_url_default(url)
        return f"Opened: {url}"

    if cmd.startswith("search "):
        q = raw.strip()[7:].strip()
        url = f"https://www.google.com/search?q={q.replace(' ','+')}"
        try: open_url_in_profile(url, "Default")
        except Exception: open_url_default(url)
        return f"Searching: {q}"

    if cmd.startswith("google ") or cmd.startswith("find "):
        q = raw.strip().split(" ",1)[1].strip()
        url = f"https://www.google.com/search?q={q.replace(' ','+')}"
        try: open_url_in_profile(url, "Default")
        except Exception: open_url_default(url)
        return f"Googled: {q}"

    if cmd.startswith("youtube "):
        q = raw.strip()[8:].strip()
        url = f"https://www.youtube.com/results?search_query={q.replace(' ','+')}"
        try: open_url_in_profile(url, "Default")
        except Exception: open_url_default(url)
        return f"YouTube: {q}"

    if cmd in ("help", "commands", "?"):
        return (
            "open <app>  |  open <site> <profile>\n"
            "search <topic>  |  google <q>  |  youtube <q>\n"
            "tab shift  |  refresh"
             )

    return f"Unknown: '{raw}'  — type help"


# ─────────────────────────────────────────────
#  GUI  — native dark title bar via Windows DWM API
# ─────────────────────────────────────────────

BG     = "#ffffff"   # body background — white
ENTRY  = "#f5f5f5"   # input background — light gray
ACCENT = "#00b09b"   # teal accent (matches title bar)
FG     = "#1a1a1a"   # text — near-black for visibility on white
MUTED  = "#888888"   # dim text — medium gray, readable on white

popup_open = False


def set_dark_titlebar(win):
    """
    Tell Windows DWM to paint the title bar dark and teal/custom colour.
    Works on Windows 10 build 19041+ and Windows 11.
    """
    try:
        hwnd = ctypes.windll.user32.GetParent(win.winfo_id())

        # Light mode flag (body is white, so disable immersive dark)
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(ctypes.c_int(0)), ctypes.sizeof(ctypes.c_int)
        )

        # Caption (title bar) background colour — teal #00b09b in BGR = 0x9BB000
        DWMWA_CAPTION_COLOR = 35
        bg_bgr = ctypes.c_int(0x009BB000)   # BGR of teal #00b09b
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_CAPTION_COLOR,
            ctypes.byref(bg_bgr), ctypes.sizeof(bg_bgr)
        )

        # Title text colour — white
        DWMWA_TEXT_COLOR = 36
        text_bgr = ctypes.c_int(0x00FFFFFF)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_TEXT_COLOR,
            ctypes.byref(text_bgr), ctypes.sizeof(text_bgr)
        )
    except Exception as e:
        print(f"DWM error (non-fatal): {e}")


def show_popup():
    global popup_open
    if popup_open:
        return
    popup_open = True

    win = tk.Tk()
    win.title("Assistant")
    win.resizable(False, False)
    win.attributes("-topmost", True)
    win.configure(bg=BG)

    W, H = 400, 100
    win.update_idletasks()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    win.geometry(f"{W}x{H}+{(sw-W)//2}+{int(sh*0.33)}")

    # Apply dark/custom title bar after window is drawn
    win.after(50, lambda: set_dark_titlebar(win))

    # ── bottom teal accent border ────────────────────────────────
    bottom_bar = tk.Frame(win, bg=ACCENT, height=3)
    bottom_bar.pack(side="bottom", fill="x")

    # ── body ────────────────────────────────────────
    body = tk.Frame(win, bg=BG, padx=12, pady=8)
    body.pack(fill="both", expand=True)

    # entry row: accent left-bar + input
    row = tk.Frame(body, bg=ENTRY, highlightbackground="#cccccc", highlightthickness=1)
    row.pack(fill="x")
    tk.Frame(row, bg=ACCENT, width=3).pack(side="left", fill="y")
    entry = tk.Entry(row, font=("Segoe UI", 11),
                     fg=FG, bg=ENTRY,
                     insertbackground=ACCENT,
                     relief="flat", bd=6,
                     highlightthickness=0)
    entry.pack(side="left", fill="x", expand=True)

    # status
    status_var = tk.StringVar(value="type a command and press Enter")
    status_lbl = tk.Label(body, textvariable=status_var,
                          font=("Segoe UI", 9), fg=MUTED,
                          bg=BG, anchor="w")
    status_lbl.pack(fill="x", pady=(6, 0))

    # hints
    hint_row = tk.Frame(body, bg=BG)
    hint_row.pack(fill="x", pady=(2, 0))
    for txt, col in [("↵ run", ACCENT), ("   Esc close", "#444444"), ("   help → all cmds", "#444444")]:
        tk.Label(hint_row, text=txt, font=("Segoe UI", 8),
                 fg=col, bg=BG).pack(side="left")

    def _grab_focus():
        """Force cursor into the entry box — beats browser/OS focus locks."""
        try:
            win.lift()
            win.attributes("-topmost", True)
            win.update_idletasks()

            # Get HWND of the tk window
            hwnd = ctypes.windll.user32.GetParent(win.winfo_id())

            # Attach our thread to the foreground thread so SetForegroundWindow works
            fg_hwnd   = ctypes.windll.user32.GetForegroundWindow()
            fg_tid    = ctypes.windll.user32.GetWindowThreadProcessId(fg_hwnd, None)
            our_tid   = ctypes.windll.kernel32.GetCurrentThreadId()
            attached  = ctypes.windll.user32.AttachThreadInput(our_tid, fg_tid, True)

            ctypes.windll.user32.AllowSetForegroundWindow(ctypes.c_uint(-1))
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            ctypes.windll.user32.BringWindowToTop(hwnd)

            if attached:
                ctypes.windll.user32.AttachThreadInput(our_tid, fg_tid, False)

            # Now tkinter focus
            win.focus_force()
            entry.focus_set()
            entry.icursor("end")
        except Exception:
            pass

    # Fire at 3 intervals — first fires before DWM animation ends,
    # last one at 350ms reliably wins even against Chrome
    win.after(50,  _grab_focus)
    win.after(150, _grab_focus)
    win.after(350, _grab_focus)

    # ── handlers ────────────────────────────────────
    def run_command(event=None):
        command = entry.get().strip()
        if not command:
            return
        status_var.set("Running…")
        status_lbl.config(fg=ACCENT)
        win.update()

        def _run():
            result = handle_command(command)
            status_var.set(result)
            ok = "Unknown" not in result
            status_lbl.config(fg=ACCENT if ok else "#cc2200")
            win.after(4000 if "\n" in result else 1800, _close)

        threading.Thread(target=_run, daemon=True).start()

    def _close():
        global popup_open
        popup_open = False
        try: win.destroy()
        except Exception: pass

    win.protocol("WM_DELETE_WINDOW", _close)
    entry.bind("<Return>", run_command)
    entry.bind("<Escape>", lambda e: _close())
    win.mainloop()


def start_listener():
    import keyboard
    keyboard.add_hotkey(
        "ctrl+shift+space",
        lambda: threading.Thread(target=show_popup, daemon=True).start(),
        suppress=True,   # prevent keystroke leaking into the active app (e.g. ChatGPT)
    )
    print(" Assistant ready — press Ctrl+Shift+Space")
    keyboard.wait()


if __name__ == "__main__":
    try:
        import keyboard
    except ImportError:
        print("Installing keyboard…")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "keyboard"])

    t = threading.Thread(target=start_listener, daemon=True)
    t.start()
    t.join()