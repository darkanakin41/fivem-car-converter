import os

if not os.path.exists(os.path.join(os.environ['LOCALAPPDATA'], "New Technology Studio\\Apps\\OpenIV\\OpenIV.exe")):
    print("OpenIV is not installed")
    exit(1)

open_iv_exe = os.path.join(
    os.environ['LOCALAPPDATA'],
    "New Technology Studio\\Apps\\OpenIV\\OpenIV.exe"
)

root_folder = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
vehicles_folder = os.path.join(root_folder, 'vehicles')
files_folder = os.path.join(root_folder, 'files')