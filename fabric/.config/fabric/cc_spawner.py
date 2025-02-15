import os

from fabric import Application
from fabric.utils import get_relative_path
from leftbar.leftbar import ControlCenter

SCRIPT_NAME = "control-center"

# lock file indicates process is running
LOCKFILE = f"/tmp/{SCRIPT_NAME}.pid"

def spawn() -> None:
    control_center = ControlCenter()
    app = Application("control-center", control_center)
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
        # If not running, start the overlay
        lock()
        spawn()
        remove_lock()  # Clean up PID file on exit
