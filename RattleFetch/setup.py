import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "tkinter"], "include_files": ["icon.ico"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "RattleFetch",
        version = "0.1",
        description = "A program that allows you to download youtube videos",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base, icon="icon.ico", target_name="RattleFetch.exe")])