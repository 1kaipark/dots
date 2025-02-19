
from bar import StatusBar 
from fabric import Application

from fabric.system_tray.widgets import SystemTray

from fabric.utils import get_relative_path 

from utils.monitors import get_all_monitors



if __name__ == "__main__":

    monitors = get_all_monitors()
    apps = []
    for monitor in monitors.keys():
        bar = StatusBar()
        bar.monitor = monitor

        app = Application("bar-{}".format(str(monitor)), bar)
        app.set_stylesheet_from_file(get_relative_path("./style.css"))

        apps.append(app)

    for app in apps:
        app.run()
