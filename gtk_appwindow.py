#!/usr/bin/env python3

import gi
import os
import sys
import threading
import time as time

gi.require_version("Gio", "2.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gio, Gtk

@Gtk.Template(filename="window.ui")
class MainWindow(Gtk.ApplicationWindow):
    
    __gtype_name__ = "window"

    button_test: Gtk.Button     = Gtk.Template.Child()
    header: Gtk.HeaderBar       = Gtk.Template.Child()
    menu_button: Gtk.MenuButton = Gtk.Template.Child()
    spinner_loading: Gtk.Spinner = Gtk.Template.Child()
    label_hello: Gtk.Label      = Gtk.Template.Child()
    revealer: Gtk.Revealer      = Gtk.Template.Child()

    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Example Window")
        self.set_default_size(600, 500)
        self.button_test.set_label("Test")
        self.set_menu_items()
        self.async_say_hello()

    def set_menu_items(self):
        menu: Gio.Menu = Gio.Menu()
        menu.append_item(Gio.MenuItem.new("Help", "app.help"))
        menu.append_item(Gio.MenuItem.new("About", "app.about"))
        menu.append_item(Gio.MenuItem.new("Quit", "app.quit"))
        self.menu_button.set_menu_model(menu)

    @Gtk.Template.Callback()
    def onButtonPressed(self, button):
        print("Hello World!")

    def say_hello(self):
        self.spinner_loading.start()
        self.revealer.set_reveal_child(True)
        time.sleep(2)
        self.revealer.set_reveal_child(False)
        self.spinner_loading.stop()

    def async_say_hello(self):
        thread = threading.Thread(target=self.say_hello, daemon=True)
        thread.start()

class BitbotApplication(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(self)
        self.win.present()
        self.win.show_all()
        
    def do_startup(self):
        Gtk.Application.do_startup(self)
        self._build_menu()

    def _build_menu(self):
        action_entries = [
            ('about', self.on_about, None),
            ("help", self.on_help, ("app.help", ["F1"])),
            ("quit", self.on_quit, ("app.quit", ["<Ctrl>Q"]))
        ]

        for action, callback, accel in action_entries:
            simple_action = Gio.SimpleAction.new(action, None)
            simple_action.connect('activate', callback)
            self.add_action(simple_action)
            if accel is not None:
                self.set_accels_for_action(*accel)
           
    def on_about(self, action, param):    
        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self.win)
        self.about.set_modal(self)
        self.about.set_authors(["Sefa Unal"])
        self.about.set_copyright("Copyright 2022 Sefa Unal")
        self.about.set_license_type(Gtk.License.GPL_3_0)
        self.about.set_website("http://sefaunal.com")
        self.about.set_website_label("http://sefaunal.com")
        self.about.set_version("0.0.1")
        self.about.set_logo_icon_name("org.sef.bitbot")
        self.about.show()
     
    def on_help(self, action, param):
        print("No one can help you!")
		
    def on_quit(self, action, param):
        dialog = Gtk.MessageDialog(transient_for=self.win,
                                   modal=True,
                                   buttons=Gtk.ButtonsType.OK_CANCEL)
        dialog.props.text = 'Are you sure you want to quit?'
        dialog.format_secondary_text("All unsaved data will be lost.")

        response = dialog.run()
        dialog.destroy()

        if (response != Gtk.ResponseType.OK):
            return

        windows = self.get_windows()
        for window in windows:
            window.destroy()
            
if __name__ == "__main__":
    app = BitbotApplication()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
