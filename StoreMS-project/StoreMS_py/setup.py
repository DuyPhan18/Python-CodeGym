import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "includes": ["tkinter"],"include_files": ["myIcon.ico"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="StoreMS",
    version="0.1",
    description="Store Management System",
    options={"build_exe": build_exe_options},
    executables=[Executable("mainapp.py", base=base, icon="myIcon.ico")]
)