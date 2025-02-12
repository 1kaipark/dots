import os

from fabric import Application
from fabric.utils import get_relative_path
from leftbar import SidePanel

from utils.monitors import get_current_gdk_monitor_id as get_focused_monitor

import setproctitle 


setproctitle.setproctitle("startpanel")
# def get_focused_monitor() -> int:
#     # efficient code bro
#     monitors = Connection().get_outputs()
# 
#     if len(monitors) == 1:
#         return 0
# 
#     for i in range(len(monitors)):
#         if monitors[i].focused:
#             return i 
# 
#     return 0

SCRIPT_NAME = "startpanel"

# lock file indicates process is running
LOCKFILE = f"/tmp/{SCRIPT_NAME}.pid"

def spawn() -> None:
    side_panel = SidePanel()
    side_panel.monitor = get_focused_monitor()
    app = Application("side-panel", side_panel)
    app.set_stylesheet_from_file(get_relative_path("./style.css"))

    app.run()

def is_locked() -> bool:
    if os.path.exists(LOCKFILE):
        with open(LOCKFILE, "r") as f:
            pid = int(f.read().strip())
            try:
                os.kill(pid, 0)  # Check if the process is running
                return True
            except ProcessLookupError:
                pass
    return False

def lock() -> None:
    with open(LOCKFILE, "w") as f:
        f.write(str(os.getpid()))

def remove_lock() -> None:
    if os.path.exists(LOCKFILE):
        os.remove(LOCKFILE)

if __name__ == "__main__":
    if is_locked():
        # kill if running
        with open(LOCKFILE, "r") as f:
            pid = int(f.read().strip())
            os.kill(pid, 9)  # SIGKILL
        remove_lock()
    else:
        lock()
        spawn()
        remove_lock()  
