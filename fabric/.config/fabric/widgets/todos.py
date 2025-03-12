from fabric import Application 
from fabric.widgets.box import Box
from fabric.widgets.wayland import WaylandWindow
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib

from fabric.utils import get_relative_path

from loguru import logger

TODOS_CACHE_PATH = GLib.get_user_cache_dir() + "/todos.txt"

class Todos(Box):

    def on_key_press(self, _, event):
        if event.keyval == 65307:
            print("Esc in entry!!")
            self.entry.set_text("")
            self.add_button.grab_focus()
            return True
        return False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        hbox = Gtk.Box(spacing=6)
        self.entry = Gtk.Entry(name="todo-entry")
        self.entry.set_placeholder_text("todos")
        self.entry.connect(
            "activate",
            self.add_todo
        )
        self.entry.connect(
            "key-press-event",
            self.on_key_press
        )

        self.add_button = Gtk.Button(label="add")
        self.add_button.connect("clicked", self.add_todo)
        hbox.pack_start(self.entry, True, True, 0)
        hbox.pack_start(self.add_button, False, False, 0)
        vbox.pack_start(hbox, False, False, 0)

        self.scrolled_window = Gtk.ScrolledWindow(name="todos-scrollable")
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(self.scrolled_window, True, True, 0)

        self.todo_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, name="todos-list")
        self.scrolled_window.add(self.todo_list)

        self.clear_button = Gtk.Button(label="clear todos")
        self.clear_button.connect("clicked", self.clear_todos)
        vbox.pack_end(self.clear_button, False, False, 0)

        self._todos: list[tuple[str, bool]] = []  # (todo_text, completed_state)

        self.load_from_cache()

    def add_todo(self, widget):
        self.add_button.grab_focus()
        todo_text = self.entry.get_text().strip()
        if todo_text:
            self._todos.append((todo_text, False))  # Initialize completion state to False
            self.cache_todos()
            self._add_todo_to_ui(todo_text, False)
            self.entry.set_text("")

    def _add_todo_to_ui(self, todo_text, completed):
        hbox = Gtk.Box(spacing=6)
        checkbox = Gtk.CheckButton(active=completed)
        label = Gtk.Label(label=todo_text, xalign=0, name="todo-label")
        label.set_xalign(0)
        if completed: 
            label.get_style_context().add_class("done")
        remove_button = Gtk.Button(label="X")
        remove_button.connect("clicked", self.remove_todo, hbox, todo_text)
        
        checkbox.connect("toggled", self.toggle_todo, label, todo_text)
        
        hbox.pack_start(checkbox, False, False, 0)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(remove_button, False, False, 0)
        
        self.todo_list.pack_start(hbox, False, False, 0)
        self.todo_list.show_all()

    def toggle_todo(self, checkbox, label, todo_text):
        style_context = label.get_style_context()
        if checkbox.get_active():
            style_context.add_class("done")
        else:
            style_context.remove_class("done")
        
        # Update the completion state in the _todos list
        for i, (text, completed) in enumerate(self._todos):
            if text == todo_text:
                self._todos[i] = (text, checkbox.get_active())
                break
        self.cache_todos()

    def remove_todo(self, widget, todo_widget, todo_text):
        self.todo_list.remove(todo_widget)
        logger.info(todo_text)
        try:
            self._todos = [(text, completed) for (text, completed) in self._todos if text != todo_text]
        except ValueError:
            logger.error("[TODOS] Error removing todo. Just clear all tbh")
        self.cache_todos()

    def clear_todos(self, widget):
        for child in self.todo_list.get_children():
            self.todo_list.remove(child)
        self._todos = []
        self.cache_todos()

    def cache_todos(self):
        try:
            with open(TODOS_CACHE_PATH, "w+") as cache:
                for todo_text, completed in self._todos:
                    cache.write(f"{todo_text}|{completed}\n")
        except Exception as e:
            logger.error("[TODOS] " + str(e))

    def load_from_cache(self):
        try:
            with open(TODOS_CACHE_PATH, "r") as cache:
                self._todos = []
                for line in cache.readlines():
                    todo_text, completed = line.strip().split("|")
                    self._todos.append((todo_text, completed == "True"))
                    self._add_todo_to_ui(todo_text, completed == "True")
        except Exception as e:
            logger.error("[TODOS] "+str(e))


if __name__ == "__main__":
    app = Application(
        "todos",
        WaylandWindow(
            name="window",
            anchor="top right",
            child=Box(children=Todos(name="todos"),name="outer-box"),
            visible=True,
            all_visible=True,
            keyboard_mode="on-demand",
        )
    )
    app.set_stylesheet_from_file(get_relative_path("./style.css"))
    app.run()
