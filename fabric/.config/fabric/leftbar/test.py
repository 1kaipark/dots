import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class Profile(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.set_homogeneous(False)
        self.set_hexpand(False)
        self.set_vexpand(False)

        profile_picture = Gtk.Box()
        profile_picture.set_halign(Gtk.Align.CENTER)
        profile_picture.set_style("background-image: url('images/profile.png');")
        self.add(profile_picture)

class Time(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_homogeneous(False)
        self.set_hexpand(False)
        self.set_vexpand(False)

        time_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        time_box.set_halign(Gtk.Align.START)
        time_box.set_hexpand(False)
        time_box.set_vexpand(False)

        hour_label = Gtk.Label()
        hour_label.set_text("12")  # Replace with actual time_hour
        time_box.add(hour_label)

        minute_label = Gtk.Label()
        minute_label.set_text("30")  # Replace with actual time_min
        time_box.add(minute_label)

        meridian_label = Gtk.Label()
        meridian_label.set_text("PM")  # Replace with actual time_mer
        time_box.add(meridian_label)

        self.add(time_box)

class Music(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.set_homogeneous(False)
        self.set_hexpand(False)
        self.set_vexpand(False)

        song_label = Gtk.Label()
        song_label.set_text("Song Name")  # Replace with actual song
        song_label.set_halign(Gtk.Align.START)
        self.add(song_label)

        artist_label = Gtk.Label()
        artist_label.set_text("Artist Name")  # Replace with actual song_artist
        artist_label.set_halign(Gtk.Align.START)
        self.add(artist_label)

class System(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=13)
        self.set_homogeneous(False)
        self.set_hexpand(False)
        self.set_vexpand(False)

        battery_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        battery_box.set_homogeneous(False)
        battery_box.set_hexpand(False)
        battery_box.set_vexpand(False)

        battery_label = Gtk.Label()
        battery_label.set_text("BAT")
        battery_box.add(battery_label)

        self.add(battery_box)

        cpu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        cpu_box.set_homogeneous(False)
        cpu_box.set_hexpand(False)
        cpu_box.set_vexpand(False)

        cpu_label = Gtk.Label()
        cpu_label.set_text("CPU")
        cpu_box.add(cpu_label)

        self.add(cpu_box)

        memory_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        memory_box.set_homogeneous(False)
        memory_box.set_hexpand(False)
        memory_box.set_vexpand(False)

        memory_label = Gtk.Label()
        memory_label.set_text("MEM")
        memory_box.add(memory_label)

        self.add(memory_box)

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Main Window")
        self.set_default_size(500, 900)
        self.set_position(Gtk.WindowPosition.CENTER)

        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.add(main_box)

        profile = Profile()
        main_box.add(profile)

        time = Time()
        main_box.add(time)

        music = Music()
        main_box.add(music)

        system = System()
        main_box.add(system)

if __name__ == "__main__":
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
