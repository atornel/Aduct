import gi

gi.require_version("GtkSource", "3.0")
from gi.repository import GtkSource
import Aduct
from Aduct import Gtk


class ButtonProvider(Aduct.Provider):
    def __init__(self):
        super().__init__("ButtonProvider")
        self.icon_names = [
            "list-add-symbolic",
            "document-new-symbolic",
            "document-save-symbolic",
            "edit-undo-symbolic",
            "edit-redo-symbolic",
            "rotation-allowed-symbolic",
            "document-edit-symbolic",
            "edit-clear-all-symbolic",
        ]

    def clear_child(self, child_dict):

        del child_dict

    def get_a_child(self, child_name):

        button_grid = Gtk.Grid(hexpand=True, margin=2)
        child_dict = {}
        child_dict["child_name"] = child_name
        child_dict["icon"] = Gtk.Image.new_from_icon_name(
            "document-properties-symbolic", 2
        )

        if child_name == "Vertical buttons":
            for y, name in enumerate(self.icon_names):
                icon = Gtk.Image.new_from_icon_name(name, 2)
                button = Gtk.Button(margin=2, relief=2)
                button.add(icon)
                button_grid.attach(button, 0, y, 1, 1)
                child_dict["header_child"] = None
                child_dict["child"] = button_grid

        elif child_name == "Horizontal buttons":
            for x, name in enumerate(self.icon_names):
                icon = Gtk.Image.new_from_icon_name(name, 2)
                button = Gtk.Button(margin=2, relief=2)
                button.add(icon)
                button_grid.attach(button, x, 0, 1, 1)
                child_dict["header_child"] = button_grid
                child_dict["child"] = Gtk.Label()

        return child_dict


class TextProvider(Aduct.Provider):
    def __init__(self):
        super().__init__("TextProvider")
        lm = GtkSource.LanguageManager()
        lang = lm.get_language("rst")
        self.buffer = GtkSource.Buffer(language=lang)

    def clear_child(self, child_dict):

        del child_dict

    def get_a_child(self, child_name):

        textview = GtkSource.View(
            editable=True, buffer=self.buffer, margin=5, expand=True
        )
        child_dict = {}
        child_dict["child_name"] = child_name
        child_dict["child"] = textview
        child_dict["header_child"] = None
        child_dict["icon"] = Gtk.Image.new_from_icon_name("text-x-generic-symbolic", 2)
        return child_dict


class ImagesProvider(Aduct.Provider):
    def __init__(self):
        super().__init__("ImagesProvider")
        self.row_names = ["Nature.png", "Seashore.jpg", "Overview.png", "Dynamite.png"]

    def clear_child(self, child_dict):

        del child_dict

    def get_a_child(self, child_name):

        title = Gtk.Label(label="<b>Images</b>", use_markup=True)
        side_grid = Gtk.Grid()
        lb = Gtk.ListBox(expand=True)
        for name in self.row_names:
            label = Gtk.Label(label=name, halign=1)
            lb.prepend(label)
        side_grid.attach(title, 0, 0, 1, 1)
        side_grid.attach(lb, 0, 1, 1, 1)
        child_dict = {}
        child_dict["child_name"] = child_name
        child_dict["child"] = side_grid
        child_dict["header_child"] = None
        child_dict["icon"] = Gtk.Image.new_from_icon_name("image-x-generic-symbolic", 2)
        return child_dict


class ViewerProvider(Aduct.Provider):
    def __init__(self):
        super().__init__("ViewerProvider")

    def clear_child(self, child_dict):

        del child_dict

    def get_a_child(self, child_name):

        img = Gtk.Image.new_from_file(
            "/home/j_arun_mani/Pictures/Abstracts and Stuff/Abstract 1.jpg"
        )
        scrolled = Gtk.ScrolledWindow(expand=True, margin=2)
        scrolled.add(img)
        child_dict = {}
        child_dict["child_name"] = child_name
        child_dict["child"] = scrolled
        child_dict["header_child"] = None
        child_dict["icon"] = Gtk.Image.new_from_icon_name(
            "applications-graphics-symbolic", 2
        )
        return child_dict


Button_Provider = ButtonProvider()
Text_Provider = TextProvider()
Images_Provider = ImagesProvider()
Viewer_Provider = ViewerProvider()

last_widget = None  # The last widget (element/notebook) where popover was shown.


def new_element():
    element = Aduct.Element(margin=5)
    element.connect("action-clicked", show_popover_element)
    # show_popover_element is a function to show the popover for an element.
    return element


def new_bin():
    bin_ = Aduct.Bin()
    return bin_


def new_paned(orientation=0):
    paned = Aduct.Paned(orientation=orientation)
    return paned


def show_popover_element(ele, but, event):

    global last_widget
    last_widget = ele

    if event == 1:  # 1 -> left-click of mouse
        prov_popover.set_relative_to(but)
        prov_popover.popup()

    elif event == 3:  # 3 -> right-click of mouse
        for modbs in tweaks.values():
            for modb in modbs:
                modb.set_sensitive(True)
        tweak_popover.set_relative_to(but)
        tweak_popover.popup()


def remove_element(wid):
    global last_widget
    Aduct.remove_element(last_widget, last_widget.get_parent())


def add_to_paned(wid, position):
    global last_widget
    element = new_element()
    paned = new_paned()
    if position == 0:
        paned.set_orientation(0)
        Aduct.add_to_paned(last_widget, element, paned, 1)
    elif position == 1:
        paned.set_orientation(0)
        Aduct.add_to_paned(last_widget, element, paned, 2)
    elif position == 2:
        paned.set_orientation(1)
        Aduct.add_to_paned(last_widget, element, paned, 1)
    elif position == 3:
        paned.set_orientation(1)
        Aduct.add_to_paned(last_widget, element, paned, 2)


def change_child_at_element(wid, prov, child_name):
    global last_widget
    Aduct.change_child_at_element(last_widget, prov, child_name)


# Making a model-button for each provider.
provs = [
    (Button_Provider, Gtk.ModelButton(text="Vertical buttons"), "Vertical buttons"),
    (Button_Provider, Gtk.ModelButton(text="Horizontal buttons"), "Horizontal buttons"),
    (Text_Provider, Gtk.ModelButton(text="Scratch pad"), "Scratch pad"),
    (Images_Provider, Gtk.ModelButton(text="Images"), "Images"),
    (Viewer_Provider, Gtk.ModelButton(text="Workspace"), "Workspace"),
]

prov_grid = Gtk.Grid()  # A grid to store them

for y, (prov, modb, child_name) in enumerate(provs):
    prov_grid.attach(modb, 0, y, 1, 1)
    modb.connect("clicked", change_child_at_element, prov, child_name)

prov_popover = Gtk.PopoverMenu()
prov_popover.add(prov_grid)
prov_grid.show_all()

# Pretty same as providers, but for tweak functions.
tweaks = {
    "Element": (Gtk.ModelButton(text="Remove"),),
    "Paned": (
        Gtk.ModelButton(text="Split left"),
        Gtk.ModelButton(text="Split right"),
        Gtk.ModelButton(text="Split up"),
        Gtk.ModelButton(text="Split down"),
    ),
}

tweak_grid = Gtk.Grid()

for x, title in enumerate(tweaks):
    label = Gtk.Label(label=title)
    tweak_grid.attach(label, x, 0, 1, 1)
    modbs = tweaks[title]
    for y, modb in enumerate(modbs):
        tweak_grid.attach(modb, x, y + 1, 1, 1)

tweak_popover = Gtk.PopoverMenu()
tweak_popover.add(tweak_grid)
tweak_grid.show_all()


def connect_tweaks():
    # Connecting model-buttons to required functions.
    elem_modb = tweaks["Element"][0]
    elem_modb.connect("clicked", remove_element)

    l_paned_modb = tweaks["Paned"][0]
    r_paned_modb = tweaks["Paned"][1]
    u_paned_modb = tweaks["Paned"][2]
    d_paned_modb = tweaks["Paned"][3]

    # 0, 1, 2, 3 are integer values of Gtk.PositionType.
    l_paned_modb.connect("clicked", add_to_paned, 0)
    r_paned_modb.connect("clicked", add_to_paned, 1)
    u_paned_modb.connect("clicked", add_to_paned, 2)
    d_paned_modb.connect("clicked", add_to_paned, 3)


connect_tweaks()

top_level = new_bin()
element = new_element()
top_level.add_child(element)  # Making a single element and adding it.

win = Gtk.Window(default_height=500, default_width=750, title="Movk Image Tool")
win.add(top_level)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
