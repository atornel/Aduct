Making an Application
=====================

No more theory, let us now get into the business of making applications.
In this tutorial we will make a very basic application that helps you in
understanding the logics. We have divided the tutorial into simpler
parts so it is easy to follow.

Since the application should be easy, we will handle only a very few
widgets of :mod:`Gtk`. The details of the widgets that are used in our providers
are given below :

-  | :class:`Gtk.Entry`
   | An entry widget takes single line input from user. It can also be
     used to display text that can only be copied but not modified. When
     the text in an entry is changed, it emits *changed* signal. To
     prevent editing the text of an entry, we set its *editable* property to
     *False.*

-  | :class:`Gtk.FileChooserButton`
   | To open, save, select files or folders we need a file chooser
     widget. After user selects a file in the file chooser dialog, a
     *file-set* signal is emitted.

-  | :class:`Gtk.Grid`
   | A grid allows packing widgets into a single widget in a tabular
     format. To attach a widget to grid, we use the gird's :func:`Gtk.Grid.attach` method.

-  | :class:`Gtk.Label`
   | Text can be displayed using a label widget. In our demo
     application, we are using only basic features of a label, that is
     *just display text*.

-  | :class:`Gtk.ModelButton`
   | Menu is often a linear list of textual buttons. To break that rule
     and include other widgets in menu, we use model buttons.

-  | :class:`Gtk.Popover`
   | Popovers are used to display something for a short period of time.
     They are usually used for drop-down menus.

-  | :class:`Gtk.ScrolledWindow`
   | If a widget is too large to be accommodated in given space, we use
     a scrolled window. This shows only the portion of the widget that
     could be displayed and rest can be scrolled.

-  | :class:`Gtk.TextBuffer`
   | Text buffer is used to store the text for a text view widget. A
     single text buffer can be shared across multiple text views.

-  | :class:`Gtk.TextView`
   | To enable multi-line text compatibility a text view widget is used.
     Text view is a front-end and the text in it is controlled using a
     text buffer. As in the case of label, we are not going to use the
     full power of a text view.

-  | :class:`Gtk.ToggleButton`
   | A toggle button is like a switch, it can have two states *active*
     and *inactive*. A *toggled* signal is emitted if the state of the
     button is changed.

-  | :class:`Gtk.Window`
   | A window is the top-level widget that represents your application.
     We quit Gtk's main loop when the main window is destroyed.

So let’s get started.

Making Providers
----------------

Providers are the core part of our application. Because of the design
philosophy of Aduct, every part of an application behaves like a
plugin. This makes an application modular in every way. To keep things
simple, we make only three providers.

-  | *Provider A*
   | It gives a text entry and a toggle button. The toggle button allows
     editing the entry.

-  | *Provider B*
   | It gives a text view and a file chooser button. The file chooser
     button opens the file for displaying.

-  | *Provider C*
   | It gives a label with text *Hello World*.

.. note:: 
    If the code to make the first two providers are difficult, then
    copy the code for Provider C and change the text for label, but the
    results will vary.

To make providers, we inherit :class:`Aduct.Provider`. Then we add the required
methods (please refer :mod:`Aduct.Provider` for more details on required
methods).

In Aduct, you will often see variables named ``child_dict``. A ``child_dict``
is of the following format.

.. code:: python

   child_dict = {
       "child": Gtk.Widget,
       "child_name": str,
       "icon": Gtk.Image,
       "header_child": Gtk.Widget or None,
       "provider": Aduct.Provider
   }

The source code for our providers are as follows. If you are lazy to copy-paste,
:download:`download <src/providers.py>` it.

.. code:: python

   import Aduct
   from Aduct import Gtk


   class Provider_A(Aduct.Provider):
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


   class Provider_B(Aduct.Provider):
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


   class Provider_C(Aduct.Provider):
       def __init__(self, name):

           super().__init__(name)

       def clear_child(self, child_props):

           del child_props

       def get_a_child(self, child_name):

           label = Gtk.Label(margin=5, label="Hello World")

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

We prefer keeping the above code in a separate file (could be named
*providers.py*), because in practical situations (while making real
applications) it is better to isolate providers from the core application,
this makes it easy to maintain. The reason we imported Gtk from Aduct
is not so crucial. It was done to reduce typing, also it makes sure that
we are using the same version of Gtk that Aduct is using.

Designing the Application
-------------------------

Now we have made providers, our next step is to frame the application.
Open a new file (could be named *app.py*). To allow widgets in the
application, we should put a way for users to view available widgets and
select the required. This is done using action button of element and
notebook. The convention is when users left-click an action button, it
should show widgets (from providers) and when they right-click, it
should show options to modify the interface.

There are two suitable ways to show the users the widgets to select
from. It could be a popup window. But pop-ups are considered
distracting. The second option is drop-down menu (also known as popover
menu). Popovers are better as they cover only a small area and are not
as annoying as popup windows. We populate the menu with model buttons.

Before adding providers, we should also spend time in a kind of
functions known as *creator functions*. As Aduct is an interface to
dynamically modify an interface, you need to be able to dynamically make
Aduct widgets. So we make small functions that, when called give the
required widget. An advantage of such functions is that they can be used
to add custom changes to widgets like changing border spacing,
connecting signals and automate other repeating tasks. The first few
lines of *app.py* is given below. (The complete file is also available for
:download:`download <src/app.py>`.)

.. code:: python
   :number-lines:

   import Aduct
   from Aduct import Gtk

   from providers import A, B, C # providers from provider.py

   last_widget = None # The last widget (element/notebook) where popover was shown.


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


   def new_notebook():
       notebook = Aduct.Notebook()
       icon = Gtk.Image.new_from_icon_name("list-add", 2)
       notebook.set_action_button(icon, 1)
       notebook.connect("action-clicked", show_popover_notebook)
       # show_popover_notebook is a function like show_popover_element.
       return notebook

The idea of the above code is simple. When action button of an element
or notebook is clicked, it emits a signal and popover is shown in
return. The popover contains model buttons for various purposes, when
they are clicked, they need to know *for which* element or notebook they
were clicked. To tackle this, when an action button is clicked, we
correspondingly set the value of ``last_widget`` to that widget. With
that, let’s append the next lines of code.

.. code:: python
   :number-lines:


   def show_popover_element(ele, but, event):

       global last_widget
       last_widget = ele

       if event == 1: # 1 -> left-click of mouse
           prov_popover.set_relative_to(but)
           prov_popover.popup()

       elif event == 3: # 3 -> right-click of mouse
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

Both the above functions are same but the difference between them is
that first one is for an element and second is for a notebook.
``prov_popover`` is for displaying widgets from providers and
``tweak_popover`` is for showing options to modify the interface. As per
the convention mentioned earlier, we show ``prov_popover`` when users
left-click and ``tweak_popover`` when users right-click an action button. We will cover
later why we are changing sensitivities of model buttons.

Now let us make some more functions that can modify the interface.

.. code:: python
   :number-lines:


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


   def add_to_notebook(wid, position):
       global last_widget
       notebook = new_notebook()
       notebook.set_tab_pos(position)
       Aduct.add_to_notebook(last_widget, notebook)

Please read :ref:`functions` to know the details of the functions
used from Aduct. Next we add more functions for changing child at an
element, saving and loading interfaces.

.. code:: python
   :number-lines:


   def change_child_at_element(wid, prov, child_name):
       global last_widget
       if last_widget.type == "element":
           Aduct.change_child_at_element(last_widget, prov, child_name)
       elif last_widget.type == "notebook":
           element = new_element()
           Aduct.change_child_at_element(element, prov, child_name)
           Aduct.add_to_notebook(element, last_widget)
           element.show_all()


   def save_interface(wid):
       from json import dump

       with open("aduct.ui", "w") as fp:
           ui_dict = Aduct.get_interface(top_level)
           dump(ui_dict, fp, indent=2)


   def load_interface(wid):
       from json import load

       with open("aduct.ui") as fp:
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
           Aduct.set_interface(ui_dict, top_level, creator_maps, init_maps)

The first function does some straight-forward tasks. It changes a child
at element when called from element. In case it is called from a
notebook, we make a new element, get a child from provider and add it
to the element. Then we append the element to the notebook.

The second function gets the interface; it is a dictionary with strings,
numbers and None. So it can be dumped using *json* in human-readable
format. We are using a file named *aduct.ui* for saving and loading
interfaces. ``top_level`` (declared later) is the view or element from
which the interface should be fetched. It is usually the root widget.

The third function surely deserves a mention. After completing this
tutorial, you can run the script (*app.py*), try playing with the
interface. Then save the interface. After that open the file named
*aduct.ui*, you will see a *JSON-styled* data with keys like *type*,
*provider* etc. Now when you ask Aduct to create the interface from the
same file, it replaces all the required values with objects (or widgets
here). The convention is that key *type* states the type of Aduct
widget and *provider* states the name of provider.

The dictionaries whose name ends with *maps*, does the job of replacing
strings or numbers with an object. They are nested-dictionaries
of depth two. It is like *what key to replace? If found replace the value
of that key with the value from maps.* For example, from ``init_maps`` we
have the key *provider.* So first the ``set_interface`` function will look
for any key named *provider* in ``ui_dict``. If found it will look at its
value, say it is *Provider A,* now it will go back to ``init_maps`` and
look for the value of key *Provider A* in the dictionary which is the value
of key named *provider*. From the above it is provider ``A``, then the function
replaces the value *Provider A* in ``ui_dict`` with the actual object;
provider ``A``. So you can consider it as a mapping of strings to
objects.

The purpose of ``creator_maps`` and ``init_maps`` are pretty same. Their
difference lies in values they are replacing. ``init_maps`` maps to
object already created, that is initialized objects, like providers,
plugins, file objects. It is to replace object that are already
available and should not created again. On the other hand,
``creator_maps``, dynamically creates objects as needed. It is for the
purpose where each object has to be unique or can be created multiple
times for multiple usage. The values of ``creator_maps`` are of this
order ``(function, args, kwargs)``. While replacing
strings with objects, the object is created by calling the function like
this : ``object = function(*args, **kwargs)``.

Pretty simple as that, however if you are confused, remember them as
mappings. That’s it.

The third function needs a root widget. It will remove whatever child it
holds and replaces it with the children from the *JSON* file. However it
returns the old child for recovering data, something not so necessary in
our application.

The finishing parts of our application is just connecting everything,
creating a new window and adding a top level view.

.. code:: python
   :number-lines:


   provs = [
       (A, Gtk.ModelButton(text="Entry"), "Entry"), # Making a model-button for each provider.
       (B, Gtk.ModelButton(text="TextView"), "TextView"),
       (C, Gtk.ModelButton(text="Label"), "Label"),
   ]

   prov_grid = Gtk.Grid() # A grid to store them

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
   top_level.add_child(element) # Making a single element and adding it.

   win = Gtk.Window(default_height=500, default_width=750)
   win.add(top_level)
   win.connect("destroy", Gtk.main_quit)
   win.show_all()
   Gtk.main()

Phew... we completed making the application! You might not have
understood some parts, but still, run the application (run *app.py*) and
see how it looks. Well just an empty screen with an empty button, right?
Click on the action button of element and add new child to the element.
Next try right clicking the action button to split it or add it to a
notebook. Have fun removing the views and adding new one. When you are
comfortable with the interface, save the interface and close the
application. Now open it again and load the interface. You should see
the interface you saved.

Let us discuss something we promised earlier. Run the application and
add an element to notebook. Now right-click the element’s action button
and click on *Add to side notebook*, you should see an error in your
terminal or console that a Aduct notebook can only have a Aduct
element as child. It is not a bug, it is a feature! Aduct notebook can
only attach a named child and the only named child in Aduct is
element. So you will get error when you try to add a child of irrelevant
type to a notebook. This is the reason we changed the sensitivities of a
few menu items. Because we don’t want to allow users to do something not
permitted. We could have made separate popovers for notebook and
element, but to avoid repeating codes with small difference, we omitted
it. You might wonder why we didn’t change sensitivities of menu items of
popovers shown for elements inside a notebook, the answer is we want you
to try!

Note a few more things which might look absurd. When you remove an
element from a paned, it collapses to a bin. When you remove
an element from notebook with three or more pages, nothing goes wrong.
But when you remove an element from a notebook with only two pages, the
notebook drops to a bin. In case of a bin, when you try to remove its
child element, instead of removing, it only clears the element.

This also has some reasons behind it. A paned is meant to hold two child, so
when you remove its one child, the purpose of a paned is destroyed, so
it becomes a bin. Similarly, a notebook is meant to hold a number of
elements and show only one of them at a time. A notebook with only page
is against its purpose, so it becomes a bin. For bin, the same logic is
applied. A Aduct bin is, by convention, used as a top-level for holding
other view. When you remove the element from it, the complete interface
link is broken and you get a blank space, where no kind of interaction
is possible. To avoid this, bin always clears the element instead of
removing it.

However, if these behaviors are not acceptable to you, you are always
free to create your own functions and use them.

While using the widgets like entry, text view in our application, you
might have noticed that an entry is just a copy of another entry, with
same text and mode, synchronized between them. This is to symbolize that
widgets with same name are basically the same. But this is not enforced.
It depends on the provider, it may produce a new widget or just a copy.

So here we reach the end of tutorial. There are some lines, paragraphs
or entire section that doesn’t even make any sense to you. Feel free to
discuss it with other developers to get help. Also if you think, the
same matter could be presented in a better manner, you are always
welcome to suggest your edits.

At last, we would like to say, designing an application is like painting.
Everyone has a brush and seven basic colors. It depends on the painter how
great he/she is going to make his/her art look. He/she may have a different ideology
and style, its unique and can’t be duplicated.

Same in case of an application, Aduct is like brush and
paint, it lies in your method, how well you are going to utilize it.
Sometimes it could come out worse, where you should surely retry.
Sometimes it could come great, where you should share the method with
others (including us!). Also beauty lies in the eyes of the viewer, not
in the painting... cheers!

