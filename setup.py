import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"
# include_files=['bg.png']
setup(  name = "socket_game",
        version = "0.1",
        description = "My GUI application!",
        # options = {"build_exe": build_exe_options},
            options={'build_exe': {'include_files': ['bg.png']}},
        executables = [Executable("game.py", base=base)])