import Qtk
from Qtk import Gtk


class Provider_A(Qtk.Provider):
    def __init__(self, name):

        super().__init__(name)
        self.text = ""
        self.toggles = []
        self.entries = []
        self.editable = False

    def change_text(self, entry):

        self.text = entry.get_text()
        for entry in self.entries:
            entry.set_text(self.text)

    def clear_child(self, child_props):

        self.entries.remove(child_props["child"])
        self.toggles.remove(child_props["header_child"])
        del child_props

    def get_a_child(self, child_name):

        entry = Gtk.Entry(margin=5, text=self.text, editable=self.editable)
        entry.connect("changed", self.change_text)

        icon = Gtk.Image.new_from_icon_name("terminal", 2)
        # Choose whatever icon you want

        switch = Gtk.ToggleButton(
            label="Allow Edit", hexpand=True, halign=2, active=self.editable
        )
        switch.connect("toggled", self.toggle_editable)

        self.entries.append(entry)
        self.toggles.append(switch)

        child_props = {
            "child_name": "Entry",
            "child": entry,
            "icon": icon,
            "header_child": switch,
        }
        return child_props

    def get_child_props(self, child_name, child, header_child):

        props = {"child_name": child_name, "text": self.text, "editable": self.editable}
        return props

    def get_child_from_props(self, props):

        self.editable = props["editable"]
        self.text = props["text"]

        for toggle in self.toggles:
            toggle.set_active(self.editable)
        for entry in self.entries:
            entry.set_editable(self.editable)
            entry.set_text(self.text)

        return self.get_a_child(props["child_name"])

    def toggle_editable(self, toggle):

        self.editable = toggle.get_active()
        for toggle in self.toggles:
            toggle.set_active(self.editable)
        for entry in self.entries:
            entry.set_editable(self.editable)


class Provider_B(Qtk.Provider):
    def __init__(self, name):

        super().__init__(name)
        self.file_choosers = []
        self.buffer = Gtk.TextBuffer()
        self.path = None

    def clear_child(self, child_props):

        self.file_choosers.remove(child_props["header_child"])
        del child_props

    def change_text_at_buffer(self, fp_but):

        path = fp_but.get_filename()
        self.path = path
        fp = open(path)
        text = fp.read()
        self.buffer.set_text(text)
        fp.close()

        for fp_chooser in self.file_choosers:
            fp_chooser.set_filename(self.path)

    def get_a_child(self, child_name):

        textview = Gtk.TextView(margin=5, buffer=self.buffer)
        scrolled = Gtk.ScrolledWindow(expand=True)
        scrolled.add(textview)

        icon = Gtk.Image.new_from_icon_name("folder", 2)

        fp_but = Gtk.FileChooserButton(title="Choose file", hexpand=True, halign=2)

        if self.path:
            fp_but.set_filename(self.path)

        fp_but.connect("file-set", self.change_text_at_buffer)
        self.file_choosers.append(fp_but)

        child_props = {
            "child_name": "TextView",
            "child": scrolled,
            "icon": icon,
            "header_child": fp_but,
        }
        return child_props

    def get_child_props(self, child_name, child, header_child):

        props = {"child_name": child_name, "path": self.path}
        return props

    def get_child_from_props(self, props):

        self.path = props["path"]
        if self.path:
            fp = open(self.path)
            text = fp.read()
            self.buffer.set_text(text)
            fp.close()

            for fp_chooser in self.file_choosers:
                fp_chooser.set_filename(self.path)

        return self.get_a_child(props["child_name"])


class Provider_C(Qtk.Provider):
    def __init__(self, name):

        super().__init__(name)

    def clear_child(self, child_props):

        del child_props

    def get_a_child(self, child_name):

        label = Gtk.Label(margin=5, label="Hello world")

        icon = Gtk.Image.new_from_icon_name("glade", 2)
        child_props = {
            "child_name": "Label",
            "child": label,
            "icon": icon,
            "header_child": None,
        }
        return child_props

    def get_child_props(self, child_name, child, header_child):

        props = {"child_name": child_name}
        return props

    def get_child_from_props(self, props):

        return self.get_a_child(props["child_name"])


A = Provider_A("Provider A")
B = Provider_B("Provider B")
C = Provider_C("Provider C")
