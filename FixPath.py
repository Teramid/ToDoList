import os

with open("ToDoList.py", "r") as f:
    f = f.readlines()


databaseFile = "ToDoList.db"
uiFile = "ToDoList.ui"
trayIconPng = "Icons\clipboard-text.png"
trayIconPng = f'trayIconPng = "{os.path.abspath(trayIconPng)}"\n'
uiFile = f'uiFile = "{os.path.abspath(uiFile)}"\n'
databaseFile = f'databaseFile = "{os.path.abspath(databaseFile)}"\n'

f[13] = databaseFile.replace("\\", "/")
f[14] = uiFile.replace("\\", "/")
f[15] = trayIconPng.replace("\\", "/")
f.pop(16)
f.pop(17)
f.pop(18)
f.insert(
    13,
    """
if sys.executable.endswith("pythonw.exe"):
\tsys.stdout = open(os.devnull, "w")
\tsys.stderr = open(os.path.join(os.getenv("TEMP"), "stderr-"+os.path.basename(sys.argv[0])), "w")\n""",
)
with open("ToDoList.pyw", "w") as f2:
    for i in f:
        f2.write(i)
