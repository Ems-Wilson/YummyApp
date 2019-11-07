import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "gql", "PIL"], "include_files":["taco-512.png"]}
# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Yummy API",
        version = "2.3.1",
        description = "I don't know what I want to eat",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Main.py", base=base, targetName="Yummy API")])