import gi

gi.require_version("GtkSource", "3.0")
from gi.repository import GtkSource
import Quanta as Qu
from Quanta import Gtk

img = Gtk.Image.new_from_file(
    "/home/j_arun_mani/Pictures/Abstracts and Stuff/Abstract 1.jpg"
)
scrolled = Gtk.ScrolledWindow(expand=True, margin=2)
scrolled.add(img)

lm = GtkSource.LanguageManager()
lang = lm.get_language("rst")
buf = GtkSource.Buffer(language=lang)
textview = GtkSource.View(editable=True, buffer=buf, margin=5)

title = Gtk.Label(label="<b>Images</b>", use_markup=True)
side_grid = Gtk.Grid()
lb = Gtk.ListBox(expand=True)
row_names = ["Nature.png", "Seashore.jpg", "Overview.png", "Dynamite.png"]
for name in row_names:
    label = Gtk.Label(label=name, halign=1)
    lb.prepend(label)
side_grid.attach(title, 0, 0, 1, 1)
side_grid.attach(lb, 0, 1, 1, 1)

button_grid = Gtk.Grid(hexpand=True, margin=2)
icon_names = [
    "list-add-symbolic",
    "document-new-symbolic",
    "document-save-symbolic",
    "edit-undo-symbolic",
    "edit-redo-symbolic",
    "rotation-allowed-symbolic",
    "document-edit-symbolic",
    "edit-clear-all-symbolic",
]
for x, name in enumerate(icon_names):
    icon = Gtk.Image.new_from_icon_name(name, 2)
    button = Gtk.Button(margin=2, relief=2)
    button.add(icon)
    button_grid.attach(button, x, 0, 1, 1)

paned1 = Gtk.Paned(orientation=0)
paned2 = Gtk.Paned(orientation=1)
paned1.add1(scrolled)
paned1.add2(side_grid)
paned2.add1(paned1)
paned2.add2(textview)

main_grid = Gtk.Grid()
main_grid.attach(button_grid, 0, 0, 1, 1)
main_grid.attach(paned2, 0, 1, 1, 1)

win = Gtk.Window(margin=2, title="Movk Image Tool", default_height=620, default_width=1220)
win.add(main_grid)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
