# ~/.ipython/profile_default/ipython_config.py — XEK profile
# Parte del bootstrap XEK-ENV v3.1.
c = get_config()  # noqa: F821

c.TerminalIPythonApp.display_banner = False
c.TerminalInteractiveShell.confirm_exit = False
c.TerminalInteractiveShell.editing_mode = "emacs"   # cambia a "vi" si prefieres
c.TerminalInteractiveShell.true_color = True
c.TerminalInteractiveShell.highlighting_style = "monokai"
c.InteractiveShell.autocall = 1
c.InteractiveShell.colors = "Linux"

c.InteractiveShellApp.extensions = ["autoreload"]
c.InteractiveShellApp.exec_lines = [
    "%autoreload 2",
    "import sys, os, json, re, io",
    "import datetime as dt",
    "from pathlib import Path",
    "from pprint import pp",
    "try:\n"
    "    import polars as pl, pandas as pd, numpy as np\n"
    "    import httpx, requests\n"
    "    from rich import print as rprint\n"
    "    from rich.console import Console\n"
    "    console = Console()\n"
    "except ImportError as _e:\n"
    "    print('XEK ipython: libs opcionales no disponibles', _e)",
]
