# Package : Aduct
# Author : J Arun Mani
# Copyright (C) 2020  J Arun Mani; Atornel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Notebook is a view that can hold only children of type :mod:`.Element`. With this
restriction, there is no limitation in number of children it can hold.
"""
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GObject, Gtk

from .View import View


class Notebook(View, Gtk.Notebook):

    __gsignals__ = {"action-clicked": (2, None, (Gtk.Button, int))}

    type = GObject.Property(type=str, default="notebook", flags=GObject.ParamFlags.READABLE)

    def __init__(self, **kwargs):

        """
        Makes a notebook based on given properties. Its CSS name is *aduct-notebook*.

        Arguments
        ---------
        **kwargs
            The values to be passed to :class:`Gtk.Notebook` from which :mod:`.Notebook` is made.

        Signals
            action-clicked
                Emitted with an integer when action button of :obj:`self` is
                clicked. The integer is 1, 2, 3 for LMB, MMB, RMB respectively.
        """

        Gtk.Notebook.__init__(self, **kwargs)
        self.set_css_name("aduct-notebook")

    def __handle_event__(self, button, event):

        self.emit("action-clicked", button, event.button)
        return True

    def add_child(self, child, position=-1):

        """
        Adds the child :obj:`self`.

        Arguments
        ---------
        child : :mod:`.Element`
            The child to be added to :obj:`self`.

        Raises
        ------
        TypeError
            Raised when :obj:`child` is not a :mod:`.Element`.
        """

        try:
            child_type = child.type
        except AttributeError:
            raise TypeError("Aduct.Notebook can only hold a child of type Aduct.Element")

        if child_type == "element":
            tab_label = self.get_tab(child)
            self.insert_page(child, tab_label, position)
        else:
            raise TypeError("Aduct.Notebook can only hold a child of type Aduct.Element")

    def change_child_label(self, child):

        """
        Changes the tab label for existing child.

        The text for new label is taken as the name of child of :obj:`child`
        (``Aduct.Element.child_name``).
        It is set to `No child` when `child` has no name for its child
        (``Aduct.Element.child_name is None``).

        Arguments
        ---------
        child : :mod:`.Element`
            The child whose tab label has to be changed.
        """

        label = self.get_tab_label(child)
        if child.child_name:
            label.set_text(child.child_name)
        else:
            label.set_text("No child")

    def get_action_button(self, pack_type):

        """
        Gets the action button at given position.

        Arguments
        ---------
        pack_type : :class:`Gtk.PackType`
            The position from which action button has to retrieved.

        Returns
        -------
        :class:`Gtk.Button` or :obj:`None`
            The action button of :obj:`self` or :obj:`None` if :obj:`self` has no action button.
        """

        return self.get_action_widget(pack_type)

    def get_tab(self, child):

        """
        Gets a tab label for child.

        The text for new label is taken as the name of child of :obj:`child`
        (``Aduct.Element.child_name``).
        It is set to `No child` when `child` has no name for its child
        (``Aduct.Element.child_name is None``).
        Based on position of tabs in :obj:`self`, the orientation of text in the label also varies.

        Arguments
        ---------
        child : :mod:`.Element`
            The child which requires a tab label.

        Returns
        -------
        :class:`Gtk.Label`
            Label with text determined from :obj:`child`.
        """

        tab_pos = self.get_tab_pos()

        top = tab_pos == Gtk.PositionType.TOP
        bottom = tab_pos == Gtk.PositionType.BOTTOM
        left = tab_pos == Gtk.PositionType.LEFT
        right = tab_pos == Gtk.PositionType.RIGHT

        if top or bottom:
            rotate = 0
        elif left or right:
            rotate = 90

        if child.child_name is None:
            name = "No child"
        else:
            name = child.child_name

        label = Gtk.Label(name="quanta-notebook-tab_label", label=name, angle=rotate)
        child.connect("child-added", self.change_child_label)
        child.connect("child-removed", self.change_child_label)
        return label

    def get_props(self):

        """
        Gets the interface properties.

        Returns
        -------
        :class:`dict`
            A dictionary with interface properties.
        """

        props = {"type": "notebook", "tab_position": self.get_tab_pos()}
        props["n_action_button"] = self.get_number_of_action_buttons()
        elements = self.get_children()
        if elements:
            for idx, element in enumerate(elements):
                element_props = element.get_props()
                props[f"element_{idx}"] = element_props
            props["n_elements"] = idx + 1
        else:
            props["n_elements"] = 0
        return props

    def get_number_of_action_buttons(self):

        """Gets the number of action buttons present.

        Returns
        -------
        :class:`int`
            The number of action buttons.
        """

        action_button_1 = self.get_action_widget(0)
        action_button_2 = self.get_action_widget(1)
        if not action_button_1 and not action_button_2:
            valid = 0
        elif action_button_1 or action_button_2:
            valid = 1
        else:
            valid = 2

        return valid

    def remove_child(self, child):

        """
        Removes the given child from :obj:`self`.

        Arguments
        ---------
        child : :mod:`.Element`
            The child which has to be removed from :obj:`self`.

        Raises
        ------
        ValueError
            Raised when :obj:`child` is not present in :obj:`self`.
        """

        if child in self.get_children():
            page_num = self.page_num(child)
            self.remove_page(page_num)
        else:
            raise ValueError("Child not in Aduct.Notebook")

    def replace_child(self, old_child, new_child):

        """
        Replaces the existing child with a new child.

        Arguments
        ---------
        old_child : :mod:`.Element`
            The child present in :obj:`self` which has to be replaced.
        new_child : :mod:`.Element`
            The child that will replace the given existing child of :obj:`self`.

        Raises
        ------
        TypeError
            Raised when :obj:`new_child` is not a :mod:`.Element`.
        """

        try:
            child_type = new_child.type
        except AttributeError:
            raise TypeError("Aduct.Notebook can only hold a child of type Aduct.Element")

        if child_type == "element":
            position = self.page_num(old_child)
            self.remove_child(old_child)
            self.add_child(new_child, position)
        else:
            raise TypeError("Aduct.Notebook can only hold a child of type Aduct.Element")

    def set_action_button(self, action_button, pack_type):

        """
        Sets the action button to notebook.

        Arguments
        ---------
        action_button : :class:`Gtk.Button`
            The button to be added to notebook. It need not be a :class:`Gtk.Button` actually,
            it could be any widget that can handle `button-press-event`.
        pack_type : :class:`Gtk.PackType`
            The position of the action button.
        """

        action_button.connect("button-press-event", self.__handle_event__)
        self.set_action_widget(action_button, pack_type)
        action_button.show_all()

    def set_from_props(self, props):

        """
        Sets the interface from given properties.

        Arguments
        ---------
        props : :class:`dict`
            The dictionary containig properties of interface.

        Raises
        ------
        ValueError
            Raised when there is a mismatch of number of action buttons in properties and
            :obj:`self`.
        """

        n_action_button = props["n_action_button"]
        valid = self.get_number_of_action_buttons()
        err = "Expected {} action button{} for Notebook as per given properties, but got {}"

        if n_action_button == 0:
            if valid == 1:
                raise ValueError(err.format(0, "s", 1))
            if valid == 2:
                raise ValueError(err.format(0, "s", 2))
        elif n_action_button == 1:
            if valid == 0:
                raise ValueError(err.format(1, "", 0))
            if valid == 2:
                raise ValueError(err.format(1, "", 2))
        elif n_action_button == 2:
            if valid == 0:
                raise ValueError(err.format(2, "s", 0))
            if valid == 1:
                raise ValueError(err.format(2, "s", 1))
        else:
            raise ValueError(
                f"Number of action buttons n: 0 <= n <= 2; but got {n_action_button}"
            )

        self.set_tab_pos(props["tab_position"])
        n_elements = props["n_elements"]

        for i in range(n_elements):
            element_i_props = props[f"element_{i}"]
            element = element_i_props["type"]
            element.set_from_props(element_i_props)
            tab_label = self.get_tab(element)
            self.append_page(element, tab_label)
