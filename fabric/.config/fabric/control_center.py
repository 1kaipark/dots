from fabric import Application
from leftbar.leftbar import ControlCenter
from fabric.utils import get_relative_path

if __name__ == "__main__":
    cc = ControlCenter()
    app = Application("control-center", cc)
    app.set_stylesheet_from_file(get_relative_path("./style.css"))
    app.run()
