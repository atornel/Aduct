import Qtk
from Qtk import Gtk

from providers import A, B, C  # providers from provider.py

last_widget = None  # The last widget (element/notebook) where popover was shown.


def new_element():
    element = Qtk.Element(margin=5)
    element.connect("action-clicked", show_popover_element)
    # show_popover_element is a function to show the popover for an element.
    return element


def new_bin():
    bin_ = Qtk.Bin()
    return bin_


def new_paned(orientation=0):
    paned = Qtk.Paned(orientation=orientation)
    return paned


def new_notebook():
    notebook = Qtk.Notebook()
    icon = Gtk.Image.new_from_icon_name("list-add", 2)
    notebook.set_action_button(icon, 1)
    notebook.connect("action-clicked", show_popover_notebook)
    # show_popover_notebook is a function like show_popover_element.
    return notebook


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


def show_popover_notebook(nb, but, event):

    global last_widget
    last_widget = nb

    if event == 1:
        prov_popover.set_relative_to(but)
        prov_popover.popup()

    elif event == 3:
        for modb in tweaks["Element"]:
            modb.set_sensitive(False)
        for modb in tweaks["Notebook"]:
            modb.set_sensitive(False)
        tweak_popover.set_relative_to(but)
        tweak_popover.popup()


def remove_element(wid):
    global last_widget
    Qtk.remove_element(last_widget, last_widget.get_parent())


def add_to_paned(wid, position):
    global last_widget
    element = new_element()
    paned = new_paned()
    if position == 0:
        paned.set_orientation(0)
        Qtk.add_to_paned(last_widget, element, paned, 1)
    elif position == 1:
        paned.set_orientation(0)
        Qtk.add_to_paned(last_widget, element, paned, 2)
    elif position == 2:
        paned.set_orientation(1)
        Qtk.add_to_paned(last_widget, element, paned, 1)
    elif position == 3:
        paned.set_orientation(1)
        Qtk.add_to_paned(last_widget, element, paned, 2)


def add_to_notebook(wid, position):
    global last_widget
    notebook = new_notebook()
    notebook.set_tab_pos(position)
    Qtk.add_to_notebook(last_widget, notebook)


def change_child_at_element(wid, prov, child_name):
    global last_widget
    if last_widget.type == "element":
        Qtk.change_child_at_element(last_widget, prov, child_name)
    elif last_widget.type == "notebook":
        element = new_element()
        Qtk.change_child_at_element(element, prov, child_name)
        Qtk.add_to_notebook(element, last_widget)
        element.show_all()


def save_interface(wid):
    from json import dump

    with open("qtk.ui", "w") as fp:
        ui_dict = Qtk.get_interface(top_level)
        dump(ui_dict, fp, indent=2)


def load_interface(wid):
    from json import load

    with open("qtk.ui") as fp:
        ui_dict = load(fp)
        creator_maps = {
            "type": {
                "element": (new_element, (), {}),
                "bin": (new_bin, (), {}),
                "notebook": (new_notebook, (), {}),
                "paned": (new_paned, (), {}),
            }
        }
        init_maps = {
            "provider": {"Provider A": A, "Provider B": B, "Provider C": C, None: None}
        }
        Qtk.set_interface(ui_dict, top_level, creator_maps, init_maps)


provs = [
    (
        A,
        Gtk.ModelButton(text="Entry"),
        "Entry",
    ),  # Making a model-button for each provider.
    (B, Gtk.ModelButton(text="TextView"), "TextView"),
    (C, Gtk.ModelButton(text="Label"), "Label"),
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
    "Notebook": (
        Gtk.ModelButton(text="Add to top notebook"),
        Gtk.ModelButton(text="Add to side notebook"),
    ),
    "Paned": (
        Gtk.ModelButton(text="Split left"),
        Gtk.ModelButton(text="Split right"),
        Gtk.ModelButton(text="Split up"),
        Gtk.ModelButton(text="Split down"),
    ),
    "Interface": (
        Gtk.ModelButton(text="Load interface"),
        Gtk.ModelButton(text="Save interface"),
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

    top_nb_modb = tweaks["Notebook"][0]
    top_nb_modb.connect("clicked", add_to_notebook, 2)
    side_nb_modb = tweaks["Notebook"][1]
    side_nb_modb.connect("clicked", add_to_notebook, 0)

    l_paned_modb = tweaks["Paned"][0]
    r_paned_modb = tweaks["Paned"][1]
    u_paned_modb = tweaks["Paned"][2]
    d_paned_modb = tweaks["Paned"][3]

    # 0, 1, 2, 3 are integer values of Gtk.PositionType.
    l_paned_modb.connect("clicked", add_to_paned, 0)
    r_paned_modb.connect("clicked", add_to_paned, 1)
    u_paned_modb.connect("clicked", add_to_paned, 2)
    d_paned_modb.connect("clicked", add_to_paned, 3)

    load_modb = tweaks["Interface"][0]
    save_modb = tweaks["Interface"][1]
    load_modb.connect("clicked", load_interface)
    save_modb.connect("clicked", save_interface)


connect_tweaks()

top_level = new_bin()
element = new_element()
top_level.add_child(element)  # Making a single element and adding it.

win = Gtk.Window(default_height=500, default_width=750)
win.add(top_level)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
