from typing import cast

from fabric import Application
from fabric import notifications
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.image import Image
from fabric.widgets.button import Button
from fabric.widgets.wayland import WaylandWindow
from fabric.notifications import Notification, Notifications
from fabric.utils import invoke_repeater, get_relative_path

from fabric.widgets.scrolledwindow import ScrolledWindow

from gi.repository import GdkPixbuf, Gtk

from loguru import logger

from fabric.utils import invoke_repeater

from services import notification_service


NOTIFICATION_IMAGE_SIZE = 64
NOTIFICATION_WIDTH = 450


class NotificationWidget(Box):
    def __init__(self, notification: Notification, popup: bool = False, **kwargs):
        super().__init__(
            size=(NOTIFICATION_WIDTH, -1),
            name="notification",
            spacing=8,
            orientation="v",
            **kwargs,
        )

        self._notification = notification

        body_container = Box(spacing=4, orientation="h")

        if self._notification.image_file:
            print(self._notification.image_file + "IMAGE FILE")

        if image_pixbuf := self._notification.image_pixbuf:
            body_container.add(
                Image(
                    pixbuf=image_pixbuf.scale_simple(
                        NOTIFICATION_IMAGE_SIZE,
                        NOTIFICATION_IMAGE_SIZE,
                        GdkPixbuf.InterpType.BILINEAR,
                    )
                )
            )
        body_container.add(
            Box(
                spacing=4,
                orientation="v",
                children=[
                    # a box for holding both the "summary" label and the "close" button
                    Box(
                        orientation="h",
                        children=[
                            Label(
                                label=self._notification.summary,
                                ellipsization="end",
                                max_chars_width=50,
                            )
                            .build()
                            .add_style_class("summary")
                            .unwrap(),
                        ],
                        #                        h_expand=True,
                        v_expand=True,
                    )
                    # add the "close" button
                    .build(
                        lambda box, _: box.pack_end(
                            Button(
                                label="x",
                                v_align="center",
                                h_align="end",
                                on_clicked=lambda *_: self._notification.close(),
                            ),
                            False,
                            False,
                            0,
                        )
                    ),
                    Label(
                        label=self._notification.body,
                        line_wrap="word-char",
                        max_chars_width=50,
                        #                        v_align="start",
                        #                        h_align="start",
                    )
                    .build()
                    .add_style_class("body")
                    .unwrap(),
                ],
                h_expand=True,
                v_expand=True,
            )
        )

        self.add(body_container)

        if actions := self._notification.actions:
            self.add(
                Box(
                    spacing=4,
                    orientation="h",
                    children=[
                        Button(
                            h_expand=True,
                            v_expand=True,
                            label=action.label,
                            on_clicked=lambda *_, action=action: action.invoke(),
                        )
                        for action in actions
                    ],
                )
            )

        # destroy this widget once the notification is closed
        self._notification.connect(
            "closed",
            lambda *_: (
                parent.remove(self) if (parent := self.get_parent()) else None,  # type: ignore
                self.destroy(),
            ),
        )
        self._notification.connect(
            "action_invoked",
            lambda *_: (
                parent.remove(self) if (parent := self.get_parent()) else None,  # type: ignore
                self.destroy(),
            ),
        )

        if self._notification.timeout >= 0:
            invoke_repeater(
                self._notification.timeout,
                lambda: self._notification.close("expired"),
                initial_call=False,
            )

        if popup:
            invoke_repeater(
                1000,
                lambda: self._notification.close("expired"),
                initial_call=False,
            )


class NotificationCenter(Box):
    def __init__(self, **kwargs):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, **kwargs)

        self.notification_service = notification_service
        self.notification_service.connect(
            "notification-added",
            self.add_noti
        )
        self.notification_service.connect(
            "notification-removed",
            self.remove_noti
        )
        self.placeholder = Label(label="...", visible=True, h_align="center")

        self.notification_list_box = Box(
            orientation="v",
            h_align="center",
            h_expand=True,
            style_classes="notification-list",
            visible=True,  # add condition for if len(self.notifications) > 0
            children=[self.placeholder],
        )

        #        self.notification_column = Box(
        #            name="notification-column",
        #            orientation="v",
        #            visible=True,
        #            size=(260, 150),
        #            children=[
        #                Label("notifications", h_align="start", style="margin: 8px;"),
        #                ScrolledWindow(
        #                    v_expand=True,
        #                    style_classes="notification-scrollable",
        #                    v_scrollbar_policy="automatic",
        #                    h_scrollbar_policy="never",
        #                    child=Box(
        #                        children=[
        #                            self.notification_list_box,
        #                        ]
        #                    ),
        #                )
        #            ]
        #        )

        self.notis_box = ScrolledWindow(
            v_expand=True,
            style_classes="notification-scrollable",
            v_scrollbar_policy="automatic",
            h_scrollbar_policy="never",
            size=(NOTIFICATION_WIDTH + 20, 150),
            child=Box(
                children=[
                    self.notification_list_box,
                ]
            ),
        )

        header_box = Box(
            children=(
                Box(
                    orientation="h",
                    children=[
                        Label(
                            label="notifications",
                        )
                        .build()
                        .unwrap(),
                    ],
                    h_expand=True,
                ).build(
                    lambda box, _: box.pack_end(
                        Button(
                            label="clear all",
                            v_align="center",
                            h_align="end",
                            on_clicked=self.clear_notis,
                        ),
                        False,
                        False,
                        0,
                    )
                ),
            ),
            h_expand=True,
            name="nc-header",
        )
        self.add(header_box)
        self.add(self.notis_box)

    def add_noti(self, notifs_service, nid):
        if len(notifs_service.notifications) > 0:
            self.placeholder.set_visible(False)
        self.notification_list_box.add(
            NotificationWidget(cast(Notification, notifs_service.notifications[nid]))
        )

    def remove_noti(self, notifs_service, nid):
        if len(notifs_service.notifications) == 0:
            self.placeholder.set_visible(True)
            
    def clear_notis(self, *_):
        n_ids = [k for k in self.notification_service.notifications.keys()]
        for n_id in n_ids:
            self.notification_service.notifications[n_id].close()


if __name__ == "__main__":
    app = Application(
        "notifications",
        WaylandWindow(
            name="window",
            margin="8px 8px 8px 8px",
            child=NotificationCenter(),
            visible=True,
            all_visible=True,
        ),
    )
    app.set_stylesheet_from_file(get_relative_path("../style.css"))

    app.run()
