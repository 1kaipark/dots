from fabric import Application
from fabric.widgets.box import Box
from fabric.widgets.wayland import WaylandWindow
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from fabric.utils import get_relative_path

from loguru import logger
from typing import Callable

TODOS_CACHE_PATH = GLib.get_user_cache_dir() + "/todos.txt"


class TodoItem(Box):
    def __init__(
        self,
        todo_text: str,
        done: bool,
        index: int,
        parent_move_up: Callable,
        parent_move_down: Callable,
        parent_remove: Callable,
        parent_toggle: Callable,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._done = done
        self._index = index
        self._parent_move_up = parent_move_up
        self._parent_move_down = parent_move_down
        self._parent_remove = parent_remove
        self._parent_toggle = parent_toggle

        self.checkbox = Gtk.CheckButton(active=self._done)
        self.label = Gtk.Label(label=todo_text, xalign=0, name="todo-label")
        self.label.set_xalign(0)
        self.label.set_max_width_chars(20)

        if self._done:
            self.label.get_style_context().add_class("done")

        self.checkbox.connect("toggled", self.toggle)

        self.up_button = Gtk.Button(label="")
        self.up_button.connect("clicked", self.on_up_clicked)

        self.down_button = Gtk.Button(label="")
        self.down_button.connect("clicked", self.on_down_clicked)

        self.remove_button = Gtk.Button(label="")
        self.remove_button.connect("clicked", self.on_remove_clicked)

        self.pack_start(self.checkbox, False, False, 0)
        self.pack_start(self.label, True, True, 0)
        self.pack_start(self.up_button, False, False, 0)
        self.pack_start(self.down_button, False, False, 0)
        self.pack_start(self.remove_button, False, False, 0)

    def toggle(self, checkbox):
        self._done = checkbox.get_active()
        if self._done:
            self.label.get_style_context().add_class("done")
        else:
            self.label.get_style_context().remove_class("done")
        self._parent_toggle(self._index, self._done)

    def on_up_clicked(self, button):
        self._parent_move_up(self._index)

    def on_down_clicked(self, button):
        self._parent_move_down(self._index)

    def on_remove_clicked(self, button):
        self._parent_remove(self._index)


class Todos(Box):
    def on_key_press(self, _, event):
        if event.keyval == 65307:  # Escape key
            print("Esc in entry!!")
            self.entry.set_text("")
            self.add_button.grab_focus()
            return True
        return False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Entry and Add button
        hbox = Gtk.Box(spacing=6)
        self.entry = Gtk.Entry(name="todo-entry")
        self.entry.set_placeholder_text("todos")
        self.entry.connect("activate", self.add_todo)
        self.entry.connect("key-press-event", self.on_key_press)

        self.add_button = Gtk.Button(label="add")
        self.add_button.connect("clicked", self.add_todo)
        hbox.pack_start(self.entry, True, True, 0)
        hbox.pack_start(self.add_button, False, False, 0)
        vbox.pack_start(hbox, False, False, 0)

        # Scrolled window for the todo list
        self.scrolled_window = Gtk.ScrolledWindow(name="todos-scrollable")
        if size := kwargs['size']:
            self.scrolled_window.set_size_request(*size)
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(self.scrolled_window, True, True, 0)

        self.todo_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, name="todos-list")
        self.scrolled_window.add(self.todo_list)

        # Clear todos button
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
            self._add_todo_to_ui(todo_text, False, len(self._todos) - 1)
            self.entry.set_text("")

    def _add_todo_to_ui(self, todo_text, completed, index):
        todo_item = TodoItem(
            todo_text=todo_text,
            done=completed,
            index=index,
            parent_move_up=self.move_todo_up,
            parent_move_down=self.move_todo_down,
            parent_remove=self.remove_todo,
            parent_toggle=self.toggle_todo,
            spacing=6,
        )
        self.todo_list.pack_start(todo_item, False, False, 0)
        self.todo_list.show_all()

    def toggle_todo(self, index, done):
        self._todos[index] = (self._todos[index][0], done)
        self.cache_todos()

    def remove_todo(self, index):
        self._todos.pop(index)
        self.refresh_ui()
        self.cache_todos()

    def move_todo_up(self, index):
        if index > 0:
            self._todos[index], self._todos[index - 1] = self._todos[index - 1], self._todos[index]
        else:
            self._todos = self._todos[1:] + [self._todos[index]]
        self.refresh_ui()
        self.cache_todos()

    def move_todo_down(self, index):
        if index < len(self._todos) - 1:
            self._todos[index], self._todos[index + 1] = self._todos[index + 1], self._todos[index]
        else:
            self._todos = [self._todos[index]] + self._todos[:-1]
        self.refresh_ui()
        self.cache_todos()

    def refresh_ui(self):
        for child in self.todo_list.get_children():
            self.todo_list.remove(child)
        for index, (todo_text, completed) in enumerate(self._todos):
            self._add_todo_to_ui(todo_text, completed, index)

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
                self.refresh_ui()
        except Exception as e:
            logger.error("[TODOS] " + str(e))


if __name__ == "__main__":
    app = Application(
        "todos",
        WaylandWindow(
            name="window",
            anchor="top right",
            child=Box(children=Todos(name="todos"), name="outer-box"),
            visible=True,
            all_visible=True,
            keyboard_mode="on-demand",
        )
    )
    app.set_stylesheet_from_file(get_relative_path("./style.css"))
    app.run()
